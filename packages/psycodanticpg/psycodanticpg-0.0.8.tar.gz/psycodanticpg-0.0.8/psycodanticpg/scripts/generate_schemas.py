from typing import Optional
from pathlib import Path
from psycodanticpg.objects.database import Database
from psycodanticpg.objects.database_url import DatabaseURL
from psycodanticpg.objects.database_schema_source import DatabaseSchemaSource
from .util.args import BaseArgsModel


class Args(BaseArgsModel):
    dsn: Optional[str] = None
    output_path: Optional[str] = None
    write_database_schemas_config: Optional[bool] = None
    write_data_types_freqlist: Optional[bool] = None


def generate_database_schemas(args: Args):
    url = DatabaseURL.parse_dsn(args.dsn)
    database = Database(url=url)
    database_schemas = database.schemas()
    database_schemas_source = DatabaseSchemaSource.parse_schemas(database_schemas)

    if args.write_database_schemas_config:
        data = database_schemas.json(indent=4)
        path = Path("test_database_schemas_config.json")
        path.write_text(data)

    if args.output_path:
        data = database_schemas_source
        path = Path(args.output_path).absolute()
        path.write_text(data)

    else:
        print("Database schemas source:\n" + database_schemas_source)


def run():
    generate_database_schemas(Args.parse_args())


if __name__ == "__main__":
    run()
