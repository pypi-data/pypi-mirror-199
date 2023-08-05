import psycopg2
import argparse
from typing import Union
from typing import Optional
from pydantic import BaseModel


class ArgsBaseModel(BaseModel):
    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser(
            description=f"Initialize {cls.__name__} from sys.argv"
        )
        for field in cls.__fields__.values():
            fieldname = field.name
            fieldtype = field.outer_type_
            parser.add_argument(
                f"--{fieldname}", type=fieldtype, help=f"{cls.__name__}.{fieldname}"
            )
        parsed_args, _ = parser.parse_known_args()
        return cls(**vars(parsed_args))


class Args(ArgsBaseModel):
    dsn: Optional[str] = None
    output_path: Optional[str] = None
    write_database_schemas_config: Optional[bool] = None
    write_data_types_freqlist: Optional[bool] = None


def generate_database_schemas(args: Args, include_schema_names: list[str] = ["public"]):
    class ColumnNameDataType(BaseModel):
        column_name: str
        sql_type: str

        @property
        def python_type(self) -> type:
            sql_type_startswith = self.sql_type.startswith
            if sql_type_startswith("character varying"):
                result = str
            elif sql_type_startswith("integer"):
                result = int
            elif sql_type_startswith("bigint"):
                result = int
            elif sql_type_startswith("text"):
                result = str
            elif sql_type_startswith("boolean"):
                result = bool
            elif sql_type_startswith("timestamp"):
                result = str
            elif sql_type_startswith("numeric"):
                result = float
            elif sql_type_startswith("ARRAY"):
                result = list
            elif sql_type_startswith("jsonb"):
                result = Union[dict, list]
                # or list
            else:
                raise ValueError(f"Unsupported SQL data type: {self.sql_type}")
            return result

        @property
        def python_typename(self) -> str:
            return self.python_type.__name__

    class DatabaseTableSchemaConfig(BaseModel):
        schema_name: str
        table_name: str
        columns: list[ColumnNameDataType]

    class DatabaseSchemaConfig(BaseModel):
        schema_name: str
        tables: list[DatabaseTableSchemaConfig]

    class DatabaseSchemasConfig(BaseModel):
        dsn: str
        data: list[DatabaseSchemaConfig]

    def db_fetchall(__dsn: str, sql: str):
        conn = psycopg2.connect(__dsn)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def fetchall_schema_names(__dsn: str):
        sql = "SELECT schema_name FROM information_schema.schemata;"
        result = db_fetchall(__dsn, sql=sql)
        return [name[0] for name in result]

    def fetchall_schema_table_names(__dsn: str, schema_name: str):
        sql = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}';"
        result = db_fetchall(__dsn, sql=sql)
        return [name[0] for name in result]

    def fetchall_tablecolumns(__dsn: str, schema_name: str, table_name: str):
        sql = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = '{schema_name}' AND table_name = '{table_name}';"
        result = db_fetchall(__dsn, sql=sql)
        return result

    dsn = args.dsn

    schema_names = fetchall_schema_names(dsn)
    print("schema_names:", schema_names)

    schema_names = [
        schema_name
        for schema_name in schema_names
        if schema_name in include_schema_names
    ]

    def get_database_schemas_config():
        result = DatabaseSchemasConfig(dsn=dsn, data=[])

        for schema_name in schema_names:
            schema_config = DatabaseSchemaConfig(schema_name=schema_name, tables=[])
            table_names = fetchall_schema_table_names(dsn, schema_name)
            print("table_names:", table_names)
            for table_name in table_names:
                table_config = DatabaseTableSchemaConfig(
                    schema_name=schema_name,
                    table_name=table_name,
                    columns=[
                        ColumnNameDataType(column_name=column[0], sql_type=column[1])
                        for column in fetchall_tablecolumns(
                            dsn, schema_name=schema_name, table_name=table_name
                        )
                    ],
                )
                schema_config.tables.append(table_config)
                print(f"{schema_name}.{table_name}")

            result.data.append(schema_config)
        return result

    def write_database_schemas_config(database_schemas_config: DatabaseSchemasConfig):
        data = database_schemas_config.json(indent=4)
        with open(f"test_database_schemas_config.json", "w+") as file:
            file.write(data)
            file.close()

    def write_data_types_freqlist(database_schemas_config: DatabaseSchemasConfig):
        from collections import Counter

        class FreqList(BaseModel):
            class KeyFreq(BaseModel):
                key: str
                freq: int

            data: list[KeyFreq]

            @classmethod
            def parse_counter(cls, counter: Counter):
                return cls(
                    data=[
                        cls.KeyFreq(key=key, freq=freq)
                        for (key, freq) in counter.most_common()
                    ]
                )

            def __iter_keys__(self):
                return (keyfreq.key for keyfreq in self.data)

            def keys(self):
                return list(self.__iter_keys__())

        data_types = Counter()
        for schema in database_schemas_config.data:
            for table in schema.tables:
                for column in table.columns:
                    data_types[column.sql_type] += 1
        freqlist = FreqList.parse_counter(data_types)
        with open(f"test_data_types.json", "w+") as file:
            file.write(freqlist.json(indent=4))
        print(freqlist.keys())

    def generate_database_schemas(database_schemas_config: DatabaseSchemasConfig):
        def get_schema_type(table: DatabaseTableSchemaConfig, offset: str = ""):
            components = []
            name = table.table_name.capitalize()
            component = f"{offset}class {name}(BaseModel):"
            components.append(component)
            fieldoffset = offset + "    "
            for column_data_type in table.columns:
                fieldname = column_data_type.column_name
                fieldtype = str(column_data_type.python_type)
                if "Union" in fieldtype and "dict, list" in fieldtype:
                    fieldtype = "(dict or list)"
                fieldtype = fieldtype.removeprefix("<class '").removesuffix("'>")
                component = f"{fieldoffset}{fieldname}: {fieldtype}"
                components.append(component)
            src = "\n".join(components)
            return src

        def get_table_schemas():
            results = []
            for schema in database_schemas_config.data:
                for table in schema.tables:
                    schema_type = get_schema_type(table)
                    results.append(schema_type)
            return results

        components = get_table_schemas()
        if components:
            components = ["from pydantic import BaseModel"] + components
        result = "\n\n".join(components) if components else ""
        if result and not result.endswith("\n"):
            result += "\n"
        return result

    database_schemas_config = get_database_schemas_config()
    if args.write_database_schemas_config:
        write_database_schemas_config(database_schemas_config)
    if args.write_data_types_freqlist:
        write_data_types_freqlist(database_schemas_config)

    database_schemas_source = generate_database_schemas(database_schemas_config)
    if args.output_path:
        from pathlib import Path

        path = Path(args.output_path).absolute()
        path.write_text(database_schemas_source)

    else:
        print("Database schemas source:\n" + database_schemas_source)


def run():
    generate_database_schemas(Args.parse_args())


if __name__ == "__main__":
    run()
