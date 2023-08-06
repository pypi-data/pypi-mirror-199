from pydantic import BaseModel
from pydantic import BaseConfig
from .sql_tablename import SQLTablename
from .schema_sql_fieldtype import SchemaSQLFieldType


class SQL(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    class Fields(BaseModel):
        fieldtypes: list[SchemaSQLFieldType]

        @property
        def names(self):
            return (fieldtype.name for fieldtype in self.fieldtypes)

        def __len__(self):
            return len(self.fieldtypes)

        def __iter__(self):
            return iter(self.fieldtypes)

    class Statements(BaseModel):
        select: str
        insert: str
        create_table: str
        drop_table: str

    tablename: SQLTablename
    fields: Fields
    statements: Statements

    @property
    def get_values_method(self):
        return lambda obj: tuple(sqlfield.from_obj(obj) for sqlfield in self.fields)
