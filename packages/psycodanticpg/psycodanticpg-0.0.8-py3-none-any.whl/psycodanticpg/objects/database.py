from typing import Optional
from typing import List
from typing import Callable
from pydantic import BaseModel
from pydantic import BaseConfig
from pydantic import Field
from psycopg2 import connect
from .database_url import DatabaseURL
from .database_schemas import DatabaseSchemas
from .schema_connection import SchemaConnection
from .some_schema import SomeSchema
from .schema_sql import SchemaSQL
from .sql_queries import SQLQueries
from .t import T


class Database(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    url: DatabaseURL = Field()
    data: dict = Field(default_factory=dict)
    queries: SQLQueries = Field(default_factory=SQLQueries)

    @property
    def dsn(self) -> str:
        return self.url.dsn

    def __get_cached__(self, key: str, getter: Callable[["Database"], T]) -> T:
        if key in self.data:
            result = self.data[key]
        else:
            result = getter(self)
            self.data[key] = result
        return result

    def __reset_data__(self):
        self.data = {}

    def __load_schemas__(self):
        conn = self.connection()
        cur = conn.cursor()
        query = self.queries["database_schemas"]
        cur.execute(query)
        raw = cur.fetchone()
        cur.close()
        conn.close()
        return DatabaseSchemas.parse_orm(raw)

    def schemas(self) -> DatabaseSchemas:
        return self.__get_cached__(
            key="schemas",
            getter=lambda database: database.__load_schemas__(),
        )

    @classmethod
    def parse_dict(cls, __dict: dict):
        return cls(url=DatabaseURL.parse_dict(__dict))

    @classmethod
    def parse_dotenv(cls, env_path: str):
        return cls(url=DatabaseURL.parse_dotenv(env_path))

    def connection(self, with_schema_connection: bool = False):
        return (SchemaConnection if with_schema_connection else connect)(self.dsn)

    def execute(
        self, query: str, commit: bool = True, with_schema_connection: bool = False
    ):
        connection = self.connection(with_schema_connection)
        cursor = connection.cursor()
        result = cursor.execute(query)
        if commit:
            connection.commit()
            self.__reset_data__()
        cursor.close()
        connection.close()
        return result

    def ping_db(self):
        conn = self.connection()
        cursor = conn.cursor()

        cursor.execute(self.queries["select_version"])
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result

    def table_names(self):
        query = self.queries["select_public_table_names"]
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        result = [record[0] for record in result]
        return result

    def table_sizes(self):
        table_names = self.table_names()
        conn = self.connection()
        results = {}
        for table_name in table_names:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            cursor.close()
            results[table_name] = count
        conn.close()
        return results

    def createtable(self, schema: SomeSchema, is_subschema: bool = False):
        if not is_subschema:
            schema_sql = SchemaSQL(schema=schema, is_subschema=is_subschema)
            sql = schema_sql.sql
            statements = sql.statements
            query = statements.create_table
            self.execute(query)

    def drop_tables(self):
        query = self.queries["drop_tables"]
        result = self.execute(query)
        return result

    def drop_table(self, schema: SomeSchema, is_subschema: bool = False):
        schema_sql = SchemaSQL(schema=schema, is_subschema=is_subschema)
        sql = schema_sql.sql
        statements = sql.statements
        query = statements.drop_table
        self.execute(query)

    def fetchone(self, schema: SomeSchema, is_subschema: bool = False):
        connection = SchemaConnection(self.url.dsn)
        schema_sql = SchemaSQL(schema=schema, is_subschema=is_subschema)
        sql = schema_sql.sql.statements.select
        result = connection.fetchone(sql, schema)
        connection.close()
        return result

    def fetchmany(
        self, schema: SomeSchema, size: Optional[int] = ..., is_subschema: bool = False
    ):
        connection = SchemaConnection(self.url.dsn)
        schema_sql = SchemaSQL(schema=schema, is_subschema=is_subschema)
        sql = schema_sql.sql.statements.select
        result = connection.fetchmany(sql, schema, size)
        connection.close()
        return result

    def fetchall(self, schema: SomeSchema, is_subschema: bool = False):
        connection = SchemaConnection(self.url.dsn)
        schema_sql = SchemaSQL(schema=schema, is_subschema=is_subschema)
        sql = schema_sql.sql.statements.select
        result = connection.fetchall(sql, schema)
        connection.close()
        return result

    def insertmany(
        self, records: List[dict], schema: SomeSchema, is_subschema: bool = False
    ):
        schema_sql = SchemaSQL(schema=schema, is_subschema=is_subschema)
        sql = schema_sql.sql.statements.insert

        models_data = [schema(**record) for record in records]
        values = [schema_sql.sql.get_values_method(obj) for obj in models_data]

        connection = SchemaConnection(self.url.dsn)
        cursor = connection.cursor()
        cursor.executemany(sql, values)
        connection.commit()
        cursor.close()
        connection.close()
