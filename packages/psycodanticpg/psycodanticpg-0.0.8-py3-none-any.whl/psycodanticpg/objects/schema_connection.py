from typing import Optional
from psycopg2.extras import DictConnection
from .some_schema import SomeSchema
from .schema_cursor import SchemaCursor


class SchemaConnection(DictConnection):
    __slots__ = ("__schema__",)

    def __with_schema_cursor__(
        self, schema: SomeSchema, sql: str, callback: SchemaCursor.Callback
    ):
        cursor = SchemaCursor(self, schema=schema)
        cursor.execute(sql)
        result = callback(cursor)
        cursor.close()
        return result

    def fetchone(self, sql: str, schema: SomeSchema):
        return self.__with_schema_cursor__(schema, sql, SchemaCursor.fetchone)

    def fetchmany(self, sql: str, schema: SomeSchema, size: Optional[int] = None):
        callback: SchemaCursor.Callback = lambda cur: cur.fetchmany(size)
        return self.__with_schema_cursor__(schema, sql, callback)

    def fetchall(self, sql: str, schema: SomeSchema):
        return self.__with_schema_cursor__(schema, sql, SchemaCursor.fetchall)
