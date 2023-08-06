from pathlib import Path
from psycopg2.sql import SQL
from psycopg2.sql import Identifier
from psycopg2.sql import Composed


def sql_dir():
    path = Path(__file__).absolute()
    return path.parent.parent.joinpath("sql")


class SQLQuery(Composed):
    @classmethod
    def parse_sql(cls, query_id: str):
        path = sql_dir().joinpath(f"{query_id}.sql")
        sql = path.read_text()
        sql = SQL(sql)
        sql.format()
        sql = sql.format(schema_names=Identifier("public"))
        return cls(sql)


class SQLQueries(dict[str, SQLQuery]):
    def __getitem__(self, __key: str):
        if __key in self:
            result: SQLQuery = dict.__getitem__(self, __key)
        else:
            result = SQLQuery.parse_sql(query_id=__key)
            self[__key] = result
        return result
