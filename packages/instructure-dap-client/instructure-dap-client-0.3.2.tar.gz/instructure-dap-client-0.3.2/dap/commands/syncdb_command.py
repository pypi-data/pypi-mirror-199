import argparse
import datetime
import logging
from typing import AsyncIterator, List, Optional

from sqlalchemy import Connection, Table, bindparam, inspect
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.asyncio import AsyncConnection

from ..api import DAPSession, DownloadError
from ..arguments import Arguments
from ..dap_types import Format, GetTableDataResult, IncrementalQuery
from ..model.metadata import MetadataRecord
from .abstract_db_command import AbstractDbCommandRegistrar, connect_to_db
from .base import ArgumentRegistrar
from .commands import SetDefaultsRegistrar
from .db_operations import DBOperations
from .models import ContextAwareObject
from .type_conversion import Operation, Record, process_resource


# Helper methods and classes
def parse_syncdb(args: Arguments) -> IncrementalQuery:
    return IncrementalQuery(
        format=Format.JSONL,
        filter=None,
        since=args.since,
        until=None,
    )


# Command registrar classes
class SyncDBCommandRegistrar(AbstractDbCommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        arguments.append(SetDefaultsRegistrar(parse_query=parse_syncdb))
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "syncdb",
                help="Performs an incremental query of a table and sends the result into a DB.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "syncdb"

    async def _execute_impl(self, args: Arguments, session: DAPSession) -> None:
        metatable_def: Table = MetadataRecord.create_metatable_def(args.namespace)

        async with connect_to_db(args.connection_string) as db_conn:
            metadata_record: MetadataRecord = await MetadataRecord.load(
                args.namespace, args.table, db_conn, metatable_def
            )
            table_def: Table = metadata_record.create_table_def()

            await db_conn.run_sync(lambda c: self._check_table(c, table_def))

            get_table_data_result = await self._get_resources(
                args, session, metadata_record
            )
            await self._save_resources(
                session, db_conn, get_table_data_result, metadata_record, table_def
            )

            await db_conn.execute(
                (
                    metatable_def.update()
                    .where(metatable_def.c.namespace == args.namespace)
                    .where(metatable_def.c.source_table == args.table)
                    .values(timestamp=bindparam("new_timestamp"))
                ),
                [
                    {
                        "new_timestamp": get_table_data_result.timestamp.astimezone(
                            datetime.timezone.utc
                        ).replace(tzinfo=None)
                    }
                ],
            )
            await db_conn.commit()

    async def _get_resources(
        self, args: Arguments, session: DAPSession, metadata_record: MetadataRecord
    ) -> GetTableDataResult:
        args.since = metadata_record.timestamp.replace(tzinfo=datetime.timezone.utc)
        query = args.parse_query(args)
        get_table_data_result = await session.get_table_data(
            args.namespace, args.table, query
        )
        return get_table_data_result

    async def _save_resources(
        self,
        session: DAPSession,
        db_conn: AsyncConnection,
        get_table_data_result: GetTableDataResult,
        metadata_record: MetadataRecord,
        table_def: Table,
    ) -> None:
        if (
            metadata_record.versioned_schema.version
            != get_table_data_result.schema_version
        ):
            raise RuntimeError(
                f"Schema version mismatch: table_data_schema_version={get_table_data_result.schema_version}, metadata_record_schema_version={metadata_record.versioned_schema.version}"
            )

        db = DBOperations(db_conn, table_def)

        job_id = get_table_data_result.job_id
        object_count = len(get_table_data_result.objects)

        for object_index, obj in enumerate(get_table_data_result.objects):
            context_aware_object = ContextAwareObject(
                id=obj.id, index=object_index, job_id=job_id, total_count=object_count
            )
            await self._download_and_save(context_aware_object, table_def, session, db)
        await db.flush()

    def _check_table(self, db_conn: Connection, table_def: Table) -> None:
        inspector: Inspector = inspect(db_conn)
        if not inspector.has_table(table_def.name, table_def.schema):
            raise RuntimeError(
                f"Table '{table_def.name}' doesn't exist in schema '{table_def.schema}'!"
            )

    async def _download_and_save(
        self,
        object: ContextAwareObject,
        table_def: Table,
        session: DAPSession,
        db: DBOperations,
    ) -> None:
        resource_array = await session.get_resources([object])
        if len(resource_array) != 1:
            raise DownloadError("unable to get resource URLs for objects")

        resource = resource_array[0]
        async with session.stream_resource(resource) as stream:
            records: AsyncIterator[Record] = process_resource(stream, table_def)

            update_count = 0
            async for record in records:
                if record.operation == Operation.Upsert:
                    await db.upsert(record.content, object)
                elif record.operation == Operation.Delete:
                    await db.delete(record.content, object)
                else:
                    raise DownloadError(f"unexpected operation: '{record.operation}'")

                update_count += 1

            if update_count == 0:
                logging.info(f"Nothing to sync {object}")
