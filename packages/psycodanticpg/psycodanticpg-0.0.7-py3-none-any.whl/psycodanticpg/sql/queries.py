from pathlib import Path
from pydantic import BaseModel
from psycopg2 import connect
from psycopg2.sql import SQL
from psycopg2.sql import Identifier
from psycopg2.sql import Composed


class SQLQuery(BaseModel):
    name: str

    def __path__(self) -> Path:
        return (
            Path(__file__)
            .absolute()
            .parent.joinpath("sql")
            .joinpath(f"{self.name}.sql")
        )

    def __query__(self):
        return self.__path__().read_text()

    @property
    def sql(self) -> Composed:
        return SQL(self.__query__()).format(schema_names=Identifier("public"))


def fetchone(dsn: str, query_name: str):
    query = SQLQuery(name=query_name)
    conn = connect(dsn)
    cursor = conn.cursor()
    cursor.execute(query.sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
