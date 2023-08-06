import enum
import json
from datetime import datetime
from typing import List, Optional, Union

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncConnection
from strong_typing.schema import JsonType, Schema
from strong_typing.serialization import json_to_object

from ..api import DAPClientError
from ..dap_types import VersionedSchema

SqlAlchemyType = Union[
    sqlalchemy.BigInteger,
    sqlalchemy.Integer,
    sqlalchemy.SmallInteger,
    sqlalchemy.Float,
    sqlalchemy.Double,
    sqlalchemy.Enum,
    sqlalchemy.TIMESTAMP,
    sqlalchemy.String,
    sqlalchemy.JSON,
    sqlalchemy.Boolean,
    sqlalchemy.ARRAY,
]


def match_type(schema: JsonType, namespace: str, table_name: str, prop_name: str):
    detected_type: Optional[SqlAlchemyType] = None

    if "oneOf" in schema:
        for oneOfTypes in schema["oneOf"]:
            if oneOfTypes["type"] != "string":
                raise OneOfTypeSchemaError(table_name)

        return sqlalchemy.String()

    if "type" not in schema:
        raise NoTypeSpecifiedError(table_name, prop_name)

    type_name = schema["type"]

    if type_name == "integer":
        if schema["format"] == "int64":
            detected_type = sqlalchemy.BigInteger()
        elif schema["format"] == "int32":
            detected_type = sqlalchemy.Integer()
        elif schema["format"] == "int16":
            detected_type = sqlalchemy.SmallInteger()

    elif type_name == "number":
        if "format" not in schema:
            detected_type = sqlalchemy.Float()

        elif schema["format"] == "float64":
            detected_type = sqlalchemy.Double()

    elif type_name == "string":
        if "enum" in schema:
            items = {item: item for item in schema["enum"]}
            enum_name = f"{table_name}__{prop_name}"
            detected_type = sqlalchemy.Enum(
                enum.Enum(enum_name, items), create_type=True, schema=namespace
            )

        elif "format" in schema and schema["format"] == "date-time":
            detected_type = sqlalchemy.TIMESTAMP(timezone=False)

        elif "maxLength" in schema:
            detected_type = sqlalchemy.String(length=schema["maxLength"])
        else:
            detected_type = sqlalchemy.String()

    elif type_name == "object":
        detected_type = sqlalchemy.JSON()

    elif type_name == "boolean":
        detected_type = sqlalchemy.Boolean()

    elif type_name == "array":
        if "items" not in schema:
            raise NoArrayItemTypeSpecifiedError(table_name, prop_name)

        items_schema = schema["items"]
        detected_type = sqlalchemy.ARRAY(
            match_type(items_schema, namespace, table_name, prop_name)
        )

    if detected_type is None:
        raise UnrecognizedTypeError(table_name, prop_name)

    return detected_type


def get_comment(schema: JsonType) -> str:
    comm = schema["description"] if "description" in schema else ""
    if type(comm) != str:
        raise NoStringDescriptionError

    return comm


class DAPSchemaParsingError(DAPClientError):
    pass


class NoStringDescriptionError(DAPSchemaParsingError):
    def __init_(self):
        super().__init__("`description` of property in schema must be a string")


class UnrecognizedTypeError(DAPSchemaParsingError):
    def __init_(self, table_name: str, prop_name: str):
        super().__init__(f"Cannot find Column type for {table_name}.{prop_name}")


class NoArrayItemTypeSpecifiedError(DAPSchemaParsingError):
    def __init_(self, table_name: str, prop_name: str):
        super().__init__(
            f"No item type is specified for array type in {table_name}.{prop_name}"
        )


class NoTypeSpecifiedError(DAPSchemaParsingError):
    def __init_(self, table_name: str, prop_name: str):
        super().__init__(
            f"Cannot recognize type without `type` field in {table_name}.{prop_name}"
        )


class CompositeKeyError(DAPSchemaParsingError):
    def __init_(self, table_name: str):
        super().__init__(f"Composite keys are not supported. Found in {table_name}")


class OneOfTypeSchemaError(DAPSchemaParsingError):
    def __init_(self, table_name: str):
        super().__init__(f"Only string is supported for oneOf types: {table_name}")


class MetadataRecord:
    namespace: str
    table_name: str
    timestamp: datetime
    versioned_schema: VersionedSchema
    metadata: sqlalchemy.MetaData

    @staticmethod
    def create_metatable_def(namespace: str) -> sqlalchemy.Table:
        metadata = sqlalchemy.MetaData(namespace)
        metatable = sqlalchemy.Table(
            "dap_meta",
            metadata,
            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
            sqlalchemy.Column("namespace", sqlalchemy.String(64), nullable=False),
            sqlalchemy.Column("source_table", sqlalchemy.String(64), nullable=False),
            sqlalchemy.Column("timestamp", sqlalchemy.DateTime(), nullable=False),
            sqlalchemy.Column("schema_version", sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column("target_schema", sqlalchemy.String(64), nullable=True),
            sqlalchemy.Column("target_table", sqlalchemy.String(64), nullable=False),
            sqlalchemy.Column(
                "schema_description_format", sqlalchemy.String(64), nullable=False
            ),
            sqlalchemy.Column("schema_description", sqlalchemy.Text(), nullable=False),
            sqlalchemy.UniqueConstraint(
                "namespace",
                "source_table",
                name="UQ__dap_meta__namespace__source_table",
            ),
        )
        return metatable

    @staticmethod
    async def load(
        namespace: str,
        table_name: str,
        db_conn: AsyncConnection,
        metatable_def: sqlalchemy.Table,
    ) -> "MetadataRecord":
        result = await db_conn.execute(
            metatable_def.select()
            .where(metatable_def.c.namespace == namespace)
            .where(metatable_def.c.source_table == table_name)
        )
        metadata_record = result.first()
        if metadata_record is None:
            raise RuntimeError(
                f"metadata not found for table `{table_name}` in `{namespace}`"
            )

        schema_description_format: str = metadata_record._mapping[
            "schema_description_format"
        ]
        if schema_description_format != "json":
            raise RuntimeError(
                f"wrong schema description format; expected: json, got: {schema_description_format}"
            )
        schema_description: JsonType = json.loads(
            metadata_record._mapping["schema_description"]
        )

        schema_version: int = metadata_record._mapping["schema_version"]
        versioned_schema: VersionedSchema = VersionedSchema(
            json_to_object(Schema, schema_description), schema_version
        )

        record: MetadataRecord = MetadataRecord(
            namespace, table_name, versioned_schema, metatable_def.metadata
        )
        record.timestamp = metadata_record._mapping["timestamp"]
        return record

    def __init__(
        self,
        namespace: str,
        table_name: str,
        versioned_schema: VersionedSchema,
        metadata: sqlalchemy.MetaData,
    ) -> None:
        self.namespace = namespace
        self.table_name = table_name
        self.versioned_schema = versioned_schema
        self.metadata = metadata

    def create_table_def(self) -> sqlalchemy.Table:
        schema = self.versioned_schema.schema["properties"]
        key_schema = schema["key"]
        key_schema_props = key_schema["properties"]

        if len(key_schema_props) != 1:
            raise CompositeKeyError(self.table_name)

        value_schema = schema["value"]
        value_schema_props = value_schema["properties"]
        columns: List[sqlalchemy.Column] = []

        required_keys = key_schema.get("required", [])
        for id_prop_name in key_schema_props:
            id_schema = key_schema_props[id_prop_name]

            column_type = match_type(
                id_schema, self.namespace, self.table_name, id_prop_name
            )

            columns.append(
                sqlalchemy.Column(
                    id_prop_name,
                    column_type,
                    primary_key=True,
                    nullable=(id_prop_name not in required_keys),
                    comment=get_comment(id_schema),
                )
            )

        required_values = value_schema.get("required", [])
        for prop_name in value_schema_props:
            prop_schema = value_schema_props[prop_name]
            column_type = match_type(
                prop_schema, self.namespace, self.table_name, prop_name
            )

            columns.append(
                sqlalchemy.Column(
                    prop_name,
                    column_type,
                    nullable=(prop_name not in required_values),
                    comment=get_comment(prop_schema),
                )
            )

        # create table model
        return sqlalchemy.Table(self.table_name, self.metadata, *columns)
