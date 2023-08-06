from enum import Enum
from typing import Any, AsyncIterator, Callable, Dict, Optional, Tuple, TypeVar

import aiohttp
from sqlalchemy import ARRAY, JSON, TIMESTAMP, BigInteger, Boolean, Column, Double
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, Integer, SmallInteger, String, Table
from strong_typing.core import JsonType

from ..payload import get_json_lines_from_gzip_stream
from ..timestamp import valid_naive_datetime

T = TypeVar("T")

# Simply Dict[str, JsonType] would be enough here, we just want to capture the presence of mandatory
# sub-structures 'key' and 'value'.
JsonRecordType = Dict[str, Dict[str, JsonType]]


def _get_optional_value(
    column_name: str, type_cast: Callable[[JsonType], Any], record_json: JsonRecordType
) -> Optional[Any]:
    "Extracts an optional value from a nullable column."

    value = record_json["value"].get(column_name)
    return type_cast(value) if value is not None else None


def _get_column_converter(col: Column) -> Callable[[JsonRecordType], Any]:
    "Returns a lambda function that extracts a column value from the JSON representation of a record."

    column_type = type(col.type)

    type_cast: Callable[[JsonType], Any]
    if (
        column_type is Integer
        or column_type is SmallInteger
        or column_type is BigInteger
    ):
        type_cast = int
    elif column_type is Float or column_type is Double:
        type_cast = float
    elif column_type is String:
        type_cast = str
    elif column_type is SqlEnum or column_type is JSON:
        type_cast = _identity
    elif column_type is TIMESTAMP:
        type_cast = valid_naive_datetime
    elif column_type is Boolean:
        type_cast = bool
    elif column_type is ARRAY:
        type_cast = _valid_list
    else:
        raise TypeError(f"cannot convert to {column_type}")

    column_name = col.name
    if col.primary_key:
        return lambda record_json: type_cast(record_json["key"][column_name])
    elif col.nullable:
        return lambda record_json: _get_optional_value(
            column_name, type_cast, record_json
        )
    else:
        return lambda record_json: type_cast(record_json["value"][column_name])


def _identity(obj: T) -> T:
    return obj


def _valid_list(obj: Any) -> list:
    if type(obj) is list:
        return obj
    else:
        raise TypeError(f"object is not a list: {obj}")


class Operation(Enum):
    Upsert = 0
    Delete = 1


class Record:
    __slots__ = "operation", "content"

    operation: Operation
    content: Dict[str, Any]

    def __init__(self, operation: Operation, content: Dict[str, Any]) -> None:
        self.operation = operation
        self.content = content


async def process_resource_for_copy(
    stream: aiohttp.StreamReader, table_def: Table
) -> AsyncIterator[Tuple]:

    # Create a tuple of converter objects for each column
    converters: Tuple = tuple(_get_column_converter(col) for col in table_def.columns)

    async for record_json in get_json_lines_from_gzip_stream(stream):
        yield tuple(converter(record_json) for converter in converters)


async def process_resource(
    stream: aiohttp.StreamReader, table_def: Table
) -> AsyncIterator[Record]:

    # create a tuple of converter objects for each column for UPSERT records
    upsert_converters = {
        col.name: _get_column_converter(col) for col in table_def.columns
    }

    # create a tuple of converter objects for each column for DELETE records
    delete_converters = {
        col.name: _get_column_converter(col) for col in table_def.primary_key
    }

    async for record_json in get_json_lines_from_gzip_stream(stream):
        if "value" in record_json:
            yield Record(
                Operation.Upsert,
                {
                    column_name: converter(record_json)
                    for column_name, converter in upsert_converters.items()
                },
            )
        else:
            yield Record(
                Operation.Delete,
                {
                    column_name: converter(record_json)
                    for column_name, converter in delete_converters.items()
                },
            )
