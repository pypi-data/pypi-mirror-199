# psycodanticpg
## psycopg2 database utilizing pydantic models
### scripts:
    psycodanticpg may be invoked as an executable file. see 'scripts' directory for all possible scripts to run using the cli.

    examples:
        to generate the pydantic schemas from an existing database, invoke the 'generate_schemas' script like this:
            python3 -m psycodanticpg generate_schemas --dsn=postgres://postgres:password@localhost:5432/mydatabase --output_path=test_generate_schema_source.py