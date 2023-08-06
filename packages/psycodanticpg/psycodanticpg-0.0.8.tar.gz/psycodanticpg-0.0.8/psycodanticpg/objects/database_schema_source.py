from .database_schema_column import DatabaseSchemaColumn
from .database_schema_table import DatabaseSchemaTable
from .database_schema import DatabaseSchema
from .database_schemas import DatabaseSchemas


class DatabaseSchemaSource(str):
    @classmethod
    def parse_column(cls, data: DatabaseSchemaColumn):
        field_name = data.column_name
        field_type = data.field_type
        result = f"    {field_name}: {field_type}"
        return cls(result)

    @classmethod
    def parse_table(cls, data: DatabaseSchemaTable):
        name = data.table_name
        columns = data.columns
        name = "".join(map(str.capitalize, name.split("_")))
        header = f"class {name}(BaseModel):"
        table_body = ""
        for column in columns:
            column_source = cls.parse_column(column)
            table_body += f"{column_source}\n"
        result = f"{header}\n{table_body}"
        return cls(result)

    @classmethod
    def parse_schema(cls, data: DatabaseSchema):
        tables = data.tables
        table_sources = [f"\n{cls.parse_table(table)}\n" for table in tables]
        result = "".join(table_sources)
        return result

    @classmethod
    def parse_schemas(cls, data: DatabaseSchemas):
        schemas = data.schemas.values()
        schema_sources = [cls.parse_schema(schema) for schema in schemas]
        source_header = "from pydantic import BaseModel"
        source_body = "".join(schema_sources)
        result = f"{source_header}\n{source_body}"
        return result
