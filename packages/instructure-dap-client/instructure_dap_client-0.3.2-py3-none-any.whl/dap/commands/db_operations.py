import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

import asyncpg
from sqlalchemy import Delete, Table, bindparam
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.dml import Insert

from ..dap_types import JobID
from .models import ContextAwareObject

RECORDS_PER_FLUSH = 300000


class _RecordSet:
    object: ContextAwareObject
    records_to_copy: List[Tuple]
    records_to_upsert: List[Dict[str, Any]]
    records_to_delete: List[Dict[str, Any]]

    def __init__(self, obj: ContextAwareObject):
        self.object = obj
        self.records_to_copy = []
        self.records_to_upsert = []
        self.records_to_delete = []


class DBOperations:
    _copy_func: Callable[[List[Tuple]], Awaitable]
    _upsert_func: Callable[[List[Dict[str, Any]]], Awaitable]
    _delete_func: Callable[[List[Dict[str, Any]]], Awaitable]

    _recordsets_per_object: Dict[str, _RecordSet]

    _record_counter: int

    def __init__(self, db_conn: AsyncConnection, table_def: Table):
        self._delete_func = self._delete(db_conn, table_def)
        self._upsert_func = self._upsert(db_conn, table_def)
        self._copy_func = self._copy(db_conn, table_def)

        self._recordsets_per_object = {}
        self._record_counter = 0

    async def copy(self, record: Tuple, obj: ContextAwareObject) -> None:
        recordset: _RecordSet = self._get_recordset(obj)
        recordset.records_to_copy.append(record)
        self._record_counter += 1
        if self._record_counter % RECORDS_PER_FLUSH == 0:
            await self.flush()

    async def upsert(self, record: Dict[str, Any], obj: ContextAwareObject) -> None:
        recordset: _RecordSet = self._get_recordset(obj)
        recordset.records_to_upsert.append(record)
        self._record_counter += 1
        if self._record_counter % RECORDS_PER_FLUSH == 0:
            await self.flush()

    async def delete(self, record: Dict[str, Any], obj: ContextAwareObject) -> None:
        recordset: _RecordSet = self._get_recordset(obj)
        recordset.records_to_delete.append(record)
        self._record_counter += 1
        if self._record_counter % RECORDS_PER_FLUSH == 0:
            await self.flush()

    async def flush(self) -> None:
        recordsets: List[_RecordSet] = list(self._recordsets_per_object.values())
        self._recordsets_per_object = {}
        self._record_counter = 0
        await self._execute_flush(recordsets)

    async def _execute_flush(self, recordsets: List[_RecordSet]) -> None:
        for recordset in recordsets:
            if recordset.records_to_copy:
                logging.debug(
                    f"Inserting {len(recordset.records_to_copy)} records from {recordset.object}"
                )
                await self._copy_func(recordset.records_to_copy)
                logging.info(
                    f"Inserted {len(recordset.records_to_copy)} records from {recordset.object}"
                )

            if recordset.records_to_upsert:
                logging.debug(
                    f"Upserting {len(recordset.records_to_upsert)} records from {recordset.object}"
                )
                await self._upsert_func(recordset.records_to_upsert)
                logging.info(
                    f"Upserted {len(recordset.records_to_upsert)} records from {recordset.object}"
                )

            if recordset.records_to_delete:
                logging.debug(
                    f"Deleting {len(recordset.records_to_delete)} records from {recordset.object}"
                )
                await self._delete_func(recordset.records_to_delete)
                logging.info(
                    f"Deleted {len(recordset.records_to_delete)} records from {recordset.object}"
                )

    def _copy(
        self, db_conn: AsyncConnection, table_def: Table
    ) -> Callable[[List[Tuple]], Awaitable]:
        if db_conn.sync_connection is None:
            raise RuntimeError("underlying database connection not found")

        driver_conn: asyncpg.connection.Connection = (
            db_conn.sync_connection.connection.driver_connection
        )

        if driver_conn is None:
            raise RuntimeError("underlying database connection not found")

        async def _copy_func(records: List[Tuple]) -> None:
            await driver_conn.copy_records_to_table(
                schema_name=table_def.metadata.schema,
                table_name=table_def.name,
                columns=[col.name for col in table_def.columns],
                records=records,
            )

        return _copy_func

    def _delete(
        self, db_conn: AsyncConnection, table_def: Table
    ) -> Callable[[List[Dict[str, Any]]], Awaitable]:
        delete_statement: Delete = table_def.delete()
        for col in table_def.primary_key:
            delete_statement = delete_statement.where(
                table_def.c[col.name] == bindparam(col.name)
            )

        async def _delete_func(records: List[Dict[str, Any]]) -> None:
            await db_conn.execute(
                statement=delete_statement,
                parameters=records,
            )

        return _delete_func

    def _upsert(
        self, db_conn: AsyncConnection, table_def: Table
    ) -> Callable[[List[Dict[str, Any]]], Awaitable]:
        upsert_statement: Insert = insert(table_def).on_conflict_do_update(
            constraint=table_def.primary_key, set_=table_def.c
        )

        async def _upsert_func(records: List[Dict[str, Any]]) -> None:
            await db_conn.execute(
                statement=upsert_statement,
                parameters=records,
            )

        return _upsert_func

    def _get_recordset(self, obj: ContextAwareObject) -> _RecordSet:
        recordset: Optional[_RecordSet] = self._recordsets_per_object.get(obj.id)
        if recordset is None:
            recordset = _RecordSet(obj)
            self._recordsets_per_object[obj.id] = recordset
        return recordset
