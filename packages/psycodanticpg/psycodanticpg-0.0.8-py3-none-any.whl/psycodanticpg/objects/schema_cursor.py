from typing import Optional
from typing import Callable
from psycopg2.extras import DictCursor
from .some_schema import SomeSchema
from .t import T


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

    Callback = Callable[["SchemaCursor"], T]
