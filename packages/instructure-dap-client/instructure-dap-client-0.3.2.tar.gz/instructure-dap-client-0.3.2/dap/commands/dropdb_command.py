import argparse
import logging
from typing import List, Optional

from sqlalchemy import Connection, Table, inspect
from sqlalchemy.engine.reflection import Inspector

from ..api import DAPSession
from ..arguments import Arguments
from ..model.metadata import MetadataRecord
from .abstract_db_command import AbstractDbCommandRegistrar, connect_to_db
from .base import ArgumentRegistrar


# Command registrar classes
class DropDBCommandRegistrar(AbstractDbCommandRegistrar):
    def __init__(self, arguments: List[ArgumentRegistrar]) -> None:
        super().__init__(arguments)

    def _create_parser(
        self, subparsers: Optional[argparse._SubParsersAction]
    ) -> Optional[argparse.ArgumentParser]:
        if subparsers is not None:
            return subparsers.add_parser(
                "dropdb",
                help="Drops the given table from the DB that was previously created with the 'initdb' command.",
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        else:
            return None

    def _can_execute_impl(self, args: Arguments) -> bool:
        return args.command == "dropdb"

    async def _execute_impl(self, args: Arguments, session: DAPSession) -> None:
        metatable_def: Table = MetadataRecord.create_metatable_def(args.namespace)

        async with connect_to_db(args.connection_string) as db_conn:
            metadata_record: MetadataRecord = await MetadataRecord.load(
                args.namespace, args.table, db_conn, metatable_def
            )
            table_def: Table = metadata_record.create_table_def()
            await db_conn.run_sync(lambda c: self._drop_table(c, table_def))

            await db_conn.execute(
                metatable_def.delete()
                .where(metatable_def.c.namespace == args.namespace)
                .where(metatable_def.c.source_table == args.table)
            )
            await db_conn.commit()

    def _drop_table(self, db_conn: Connection, table_def: Table) -> None:
        inspector: Inspector = inspect(db_conn)
        if not inspector.has_table(table_def.name, table_def.schema):
            raise RuntimeError(
                f"table `{table_def.name}` does not exist in schema `{table_def.schema}`"
            )

        table_def.drop(db_conn)
