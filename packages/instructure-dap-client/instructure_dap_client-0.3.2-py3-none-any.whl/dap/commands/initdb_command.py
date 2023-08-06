import argparse
import logging
from datetime import timezone
from typing import AsyncIterator, List, Optional, Tuple

from sqlalchemy import Connection, Table, inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.schema import CreateSchema
from strong_typing.serialization import json_dump_string

from ..api import DAPSession, DownloadError
from ..arguments import Arguments
from ..concurrency import wait_n
from ..dap_types import Format, GetTableDataResult, Object, SnapshotQuery
from ..model.metadata import MetadataRecord
from .abstract_db_command import AbstractDbCommandRegistrar, connect_to_db
from .base import ArgumentRegistrar
from .commands import SetDefaultsRegistrar
from .db_operations import DBOperations
from .models import ContextAwareObject
from .type_conversion import process_resource_for_copy

CONCURRENCY: int = 4


# Helper methods and classes
def parse_initdb(args: Arguments) -> SnapshotQuery:
    return SnapshotQuery(format=Format.JSONL, filter=None)


# Command registrar classes
class InitDBCommandRegistrar(AbstractDbCommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        arguments.append(SetDefaultsRegistrar(parse_query=parse_initdb))
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "initdb",
                help="Performs a snapshot query of a table and sends the result into a DB.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "initdb"

    async def _execute_impl(self, args: Arguments, session: DAPSession) -> None:
        async with connect_to_db(args.connection_string) as db_conn:
            await db_conn.run_sync(
                lambda c: self._check_table(c, args.table, args.namespace)
            )

            get_table_data_result = await self._get_resources(args, session)
            await self._save_resources(args, session, db_conn, get_table_data_result)

            await db_conn.commit()

    async def _get_resources(
        self, args: Arguments, session: DAPSession
    ) -> GetTableDataResult:
        query = args.parse_query(args)
        get_table_data_result = await session.get_table_data(
            args.namespace, args.table, query
        )
        return get_table_data_result

    async def _save_resources(
        self,
        args: Arguments,
        session: DAPSession,
        db_conn: AsyncConnection,
        get_table_data_result: GetTableDataResult,
    ) -> None:
        table_schema = await session.get_table_schema(args.namespace, args.table)
        if table_schema.version != get_table_data_result.schema_version:
            raise RuntimeError(
                f"schema version mismatch; expected: {table_schema.version}, got: {get_table_data_result.schema_version}"
            )

        metatable_def: Table = MetadataRecord.create_metatable_def(args.namespace)
        metadata_record: MetadataRecord = MetadataRecord(
            args.namespace, args.table, table_schema, metatable_def.metadata
        )
        table_def: Table = metadata_record.create_table_def()

        await db_conn.run_sync(lambda c: self._create_tables(c, table_def))

        db = DBOperations(db_conn, table_def)

        object_count = len(get_table_data_result.objects)
        job_id = get_table_data_result.job_id

        async def logged_download_and_save(obj: Object, object_index: int):
            context_aware_object = ContextAwareObject(
                id=obj.id, index=object_index, job_id=job_id, total_count=object_count
            )
            await self._download_and_save(context_aware_object, table_def, session, db)

        await wait_n(
            [
                logged_download_and_save(obj, obj_index)
                for obj_index, obj in enumerate(get_table_data_result.objects)
            ],
            concurrency=CONCURRENCY,
        )
        await db.flush()

        await db_conn.execute(
            metatable_def.insert(),
            [
                {
                    "namespace": args.namespace,
                    "source_table": args.table,
                    "timestamp": get_table_data_result.timestamp.astimezone(
                        timezone.utc
                    ).replace(tzinfo=None),
                    "schema_version": get_table_data_result.schema_version,
                    "target_schema": table_def.schema,
                    "target_table": table_def.name,
                    "schema_description_format": "json",
                    "schema_description": json_dump_string(table_schema.schema),
                }
            ],
        )

    def _check_table(
        self, db_conn: Connection, table_name: str, table_schema: str
    ) -> None:
        inspector: Inspector = inspect(db_conn)
        if inspector.has_table(table_name, table_schema):
            raise RuntimeError(
                f"table `{table_name}` already exists in schema `{table_schema}`"
            )

    def _create_tables(self, db_conn: Connection, table_def: Table) -> None:
        inspector: Inspector = inspect(db_conn)
        if table_def.schema is not None and not inspector.has_schema(table_def.schema):
            db_conn.execute(CreateSchema(table_def.schema))

        table_def.metadata.create_all(db_conn)

    async def _download_and_save(
        self,
        obj: ContextAwareObject,
        table_def: Table,
        session: DAPSession,
        db: DBOperations,
    ) -> None:
        resource_array = await session.get_resources([Object(obj.id)])
        if len(resource_array) != 1:
            raise DownloadError("unable to get resource URLs for objects")

        logging.info(f"Downloading {obj}")

        resource = resource_array[0]
        async with session.stream_resource(resource) as stream:
            records: AsyncIterator[Tuple] = process_resource_for_copy(stream, table_def)

            async for record in records:
                await db.copy(record, obj)
