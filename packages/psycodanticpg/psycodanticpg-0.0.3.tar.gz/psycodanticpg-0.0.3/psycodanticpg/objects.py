import uuid
import datetime
import dataclasses
from typing import Optional
from typing import TypeVar
from typing import Callable
from typing import List
from typing import Any
from decimal import Decimal
from pydantic import BaseModel
from pydantic import BaseConfig
from dotenv import dotenv_values
from psycopg2 import connect
from psycopg2.extras import DictConnection
from psycopg2.extras import DictCursor
from psycopg2.extras import Json

SomeSchema = TypeVar("SomeSchema", bound=BaseModel)

T = TypeVar("T")


class SchemaSQLFieldType(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    fieldname: str
    fieldtype: Any

    @property
    def sql_type(self) -> str:
        fieldtype = self.fieldtype
        try:
            typename = fieldtype.__name__
        except:
            typename = ""
        typename_lower = typename.lower()
        for type_prefix, result_type in (
            ("int", "int"),
            ("float", "real"),
            ("str", "varchar"),
            ("bool", "boolean"),
            ("dict", "jsonb"),
        ):
            if typename_lower.startswith(type_prefix):
                result = result_type
                break
        else:
            for match_type, result_type in (
                (int, "int"),
                (float, "real"),
                (str, "varchar"),
                (bool, "boolean"),
                (datetime.date, "date"),
                (datetime.time, "time"),
                (datetime.datetime, "timestamp"),
                (uuid.UUID, "uuid"),
                (bytes, "bytea"),
                (Decimal, "numeric"),
                (dict, "jsonb"),
                (list, "jsonb"),
            ):
                if fieldtype == match_type:
                    result = result_type
                    break
            else:
                raise ValueError(f"Unsupported Pydantic type: {fieldtype}")
        return result

    def from_obj(self, obj):
        result = getattr(obj, self.fieldname)
        if self.sql_type == "jsonb":
            result = Json(result)
        return result


class SQL(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    class SQLFields(BaseModel):
        fieldtypes: list[SchemaSQLFieldType]

        @property
        def names(self):
            return (fieldtype.fieldname for fieldtype in self.fieldtypes)

        def __len__(self):
            return len(self.fieldtypes)

        def __iter__(self):
            return iter(self.fieldtypes)

    class SQLStatements(BaseModel):
        select: str
        insert: str
        create_table: str
        drop_table: str

    tablename: str
    fields: SQLFields
    statements: SQLStatements

    @property
    def get_values_method(self):
        return lambda obj: tuple(sqlfield.from_obj(obj) for sqlfield in self.fields)


@dataclasses.dataclass(frozen=False, order=True)
class SchemaSQL:
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    _schema: Any
    _sql: Optional[SQL] = None

    def __init__(self, schema: SomeSchema, sql: Optional[SQL] = None) -> None:
        self._schema, self._sql = schema, sql

    @property
    def schema(self) -> SomeSchema:
        return self._schema

    @property
    def sql(self) -> SQL:
        result = self._sql
        if result is None:
            schema = self.schema
            tablename = str(schema.__name__)
            if "." in tablename:
                tablename = tablename[tablename.rindex(".") + 1 :]
            tablename = tablename[
                : next(
                    (i for (i, letter) in enumerate(tablename[1:]) if letter.isupper()),
                    len(tablename) - 1,
                )
                + 1
            ].lower()

            fields = SQL.SQLFields(
                fieldtypes=[
                    SchemaSQLFieldType(
                        fieldname=field.name, fieldtype=field.outer_type_
                    )
                    for field in schema.__fields__.values()
                ]
            )

            fieldnames_string = ", ".join(fields.names)
            abstract_values = ", ".join("%s" for _ in range(0, len(fields)))
            select = f"SELECT {fieldnames_string} FROM {tablename}"
            insert = f"INSERT INTO {tablename} ({fieldnames_string}) VALUES ({abstract_values})"
            create_table = f"CREATE TABLE {tablename} ({', '.join(f'{field.fieldname} {field.sql_type}' for field in fields)});"
            drop_table = f"DROP TABLE IF EXISTS {tablename};"
            statements = SQL.SQLStatements(
                select=select,
                insert=insert,
                create_table=create_table,
                drop_table=drop_table,
            )

            result = SQL(tablename=tablename, fields=fields, statements=statements)
            self._sql = result
        return result


class DatabaseURL(BaseModel):
    DATABASE_DRIVER: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str

    @property
    def dsn(self):
        dsn = f"{self.DATABASE_DRIVER}://"
        if self.DATABASE_USER and self.DATABASE_PASSWORD:
            dsn += f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
        dsn += self.DATABASE_HOST
        if self.DATABASE_PORT:
            dsn += f":{self.DATABASE_PORT}"
        dsn += f"/{self.DATABASE_NAME}"
        return dsn

    @classmethod
    def parse_dict(cls, __dict: dict):
        return cls(**{key: __dict.get(key) for key in cls.__fields__.keys()})

    @classmethod
    def parse_dotenv(cls, env_path: str):
        return cls.parse_dict(dict(dotenv_values(env_path).items()))


class SchemaCursor(DictCursor):
    __slots__ = ("__schema__",)

    def __init__(self, *args, schema: SomeSchema, **kwargs):
        super().__init__(*args, **kwargs)
        self.__schema__ = schema

    def __format_one__(self, record: Optional[dict] = None):
        return self.__schema__.parse_obj(record)

    def __format_many__(self, records: list[dict]):
        return [self.__schema__.parse_obj(record) for record in records]

    def fetchone(self):
        record = super().fetchone()
        return record if record is None else self.__format_one__(record)

    def fetchmany(self, size: Optional[int] = None):
        return self.__format_many__(super().fetchmany(size))

    def fetchall(self):
        return self.__format_many__(super().fetchall())


class SchemaConnection(DictConnection):
    __slots__ = ("__schema__",)

    def __with_schema_cursor__(
        self, schema: SomeSchema, sql: str, process_result: Callable[[SchemaCursor], T]
    ):
        cursor = SchemaCursor(self, schema=schema)
        cursor.execute(sql)
        result = process_result(cursor)
        cursor.close()
        return result

    def fetchone(self, sql: str, schema: SomeSchema):
        return self.__with_schema_cursor__(schema, sql, SchemaCursor.fetchone)

    def fetchmany(self, sql: str, schema: SomeSchema, size: Optional[int] = None):
        return self.__with_schema_cursor__(
            schema, sql, lambda cursor: cursor.fetchmany(size)
        )

    def fetchall(self, sql: str, schema: SomeSchema):
        return self.__with_schema_cursor__(schema, sql, SchemaCursor.fetchall)


class Database(BaseModel):
    url: DatabaseURL

    @classmethod
    def parse_dict(cls, __dict: dict):
        return cls(url=DatabaseURL.parse_dict(__dict))

    @classmethod
    def parse_dotenv(cls, env_path: str):
        return cls(url=DatabaseURL.parse_dotenv(env_path))

    @property
    def dsn(self) -> str:
        return self.url.dsn

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
        cursor.close()
        connection.close()
        return result

    def ping_db(self, sql: str = "SELECT version();"):
        conn = self.connection()
        cursor = conn.cursor()

        cursor.execute(sql)
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result

    def createtable(self, schema: SomeSchema):
        schema_sql = SchemaSQL(schema=schema)
        sql = schema_sql.sql
        statements = sql.statements
        query = statements.create_table

        self.execute(query)

    def droptable(self, schema: SomeSchema):
        print("SCHEMA:", schema)
        schema_sql = SchemaSQL(schema=schema)
        sql = schema_sql.sql
        statements = sql.statements
        query = statements.drop_table

        self.execute(query)

    def fetchone(self, schema: SomeSchema):
        connection = SchemaConnection(self.url.dsn)
        schema_sql = SchemaSQL(schema=schema)
        sql = schema_sql.sql.statements.select
        result = connection.fetchone(sql, schema)
        connection.close()
        return result

    def fetchmany(self, schema: SomeSchema, size: Optional[int] = ...):
        connection = SchemaConnection(self.url.dsn)
        schema_sql = SchemaSQL(schema=schema)
        sql = schema_sql.sql.statements.select
        result = connection.fetchmany(sql, schema, size)
        connection.close()
        return result

    def fetchall(self, schema: SomeSchema):
        connection = SchemaConnection(self.url.dsn)
        schema_sql = SchemaSQL(schema=schema)
        sql = schema_sql.sql.statements.select
        result = connection.fetchall(sql, schema)
        connection.close()
        return result

    def insertmany(self, records: List[dict], schema: SomeSchema):
        schema_sql = SchemaSQL(schema=schema)
        sql = schema_sql.sql.statements.insert

        models_data = [schema(**record) for record in records]
        values = [schema_sql.sql.get_values_method(obj) for obj in models_data]

        connection = SchemaConnection(self.url.dsn)
        cursor = connection.cursor()
        cursor.executemany(sql, values)
        connection.commit()
        cursor.close()
        connection.close()
