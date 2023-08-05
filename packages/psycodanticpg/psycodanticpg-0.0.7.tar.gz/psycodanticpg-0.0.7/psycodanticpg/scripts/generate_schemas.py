import json
import argparse
from typing import List
from typing import Optional
from pathlib import Path
from pydantic import BaseModel
from psycodanticpg.sql import queries


class Args(BaseModel):
    dsn: Optional[str] = None
    output_path: Optional[str] = None
    write_database_schemas_config: Optional[bool] = None
    write_data_types_freqlist: Optional[bool] = None

    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser()
        for field in cls.__fields__.values():
            type, help = field.outer_type_, f"{cls.__name__}.{field.name}"
            parser.add_argument(f"--{field.name}", type=type, help=help)
        parsed_args, _ = parser.parse_known_args()
        return cls(**vars(parsed_args))


class DatabaseSchemas(BaseModel):
    class SchemaData(BaseModel):
        class TableData(BaseModel):
            class ColumnData(BaseModel):
                column_name: str
                data_type: str
                field_type: str

            table_name: str
            columns: List[ColumnData]

        schema_name: str
        tables: List[TableData]

    dsn: str
    schemas: dict[str, SchemaData]


def generate_database_schemas(args: Args):
    dsn = args.dsn
    schemas = queries.fetchone(dsn=dsn, query_name="database_schemas")
    if schemas is not None:
        schemas = schemas[0]
        if schemas is not None:
            data = json.dumps(dict(dsn=dsn, schemas=schemas))
            schemas = DatabaseSchemas.parse_raw(data, content_type="json")
    source = "from pydantic import BaseModel\n"
    format_column = lambda column: f"    {column.column_name}: {column.field_type}"
    for schema in schemas.schemas.values():
        for table in schema.tables:
            tablename = "".join(map(str.capitalize, table.table_name.split("_")))
            columns = "\n".join(map(format_column, table.columns))
            source += f"\nclass {tablename}(BaseModel):\n{columns}\n"

    if args.write_database_schemas_config:
        data = schemas.json(indent=4)
        Path("test_database_schemas_config.json").write_text(data)
    if args.output_path:
        Path(args.output_path).absolute().write_text(source)
    else:
        print("Database schemas source:\n" + source)


def run():
    generate_database_schemas(Args.parse_args())


if __name__ == "__main__":
    run()
