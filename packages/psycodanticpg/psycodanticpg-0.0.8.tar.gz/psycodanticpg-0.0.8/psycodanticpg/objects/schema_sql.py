import dataclasses
from typing import Optional
from typing import TypeVar
from typing import Any
from pydantic import BaseModel
from pydantic import BaseConfig
from .sql import SQL
from .sql_tablename import SQLTablename
from .schema_sql_fieldtype import SchemaSQLFieldType

SomeSchema = TypeVar("SomeSchema", bound=BaseModel)


@dataclasses.dataclass(frozen=False, order=True)
class SchemaSQL:
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    _schema: Any
    _sql: Optional[SQL] = None
    _is_subschema: bool = False

    def __init__(
        self, schema: SomeSchema, sql: Optional[SQL] = None, is_subschema: bool = False
    ) -> None:
        self._schema = schema
        self._sql = sql
        self._is_subschema = is_subschema

    @property
    def is_subschema(self) -> bool:
        return self._is_subschema

    @property
    def schema(self) -> SomeSchema:
        return self._schema

    @property
    def sql(self) -> SQL:
        result = self._sql
        if result is None:
            schema = self.schema
            tablename = SQLTablename(schema.__name__)

            fields = SQL.Fields(
                fieldtypes=[
                    SchemaSQLFieldType(name=field.name, field_type=field.outer_type_)
                    for field in schema.__fields__.values()
                ]
            )

            fieldnames_string = ", ".join(fields.names)
            abstract_values = ", ".join("%s" for _ in range(0, len(fields)))

            db_tablename = (
                tablename.parent_tablename
                if self.is_subschema
                else tablename.snake_cased
            )

            select = f"SELECT {fieldnames_string} FROM {db_tablename}"
            insert = f"INSERT INTO {db_tablename} ({fieldnames_string}) VALUES ({abstract_values})"
            create_table = f"CREATE TABLE {db_tablename} ({', '.join(f'{field.name} {field.sql_type}' for field in fields)});"
            drop_table = f"DROP TABLE IF EXISTS {db_tablename};"
            statements = SQL.Statements(
                select=select,
                insert=insert,
                create_table=create_table,
                drop_table=drop_table,
            )

            result = SQL(tablename=tablename, fields=fields, statements=statements)
            self._sql = result
        return result
