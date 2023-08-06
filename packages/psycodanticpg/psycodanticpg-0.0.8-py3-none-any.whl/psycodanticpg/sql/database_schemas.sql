WITH schema_names AS (
    SELECT schema_name 
    FROM information_schema.schemata
), 
schema_tablenames AS (
    SELECT table_schema, table_name 
    FROM information_schema.tables 
    WHERE table_schema IN ('public','custom') 
)
SELECT 
    json_build_object(
        schema_tablenames.table_schema,
        json_build_object(
            'schema_name', schema_tablenames.table_schema,
            'tables', json_agg(
                json_build_object(
                    'table_name', schema_tablenames.table_name,
                    'columns', columns
                )
            )
        )
    ) AS schema_data
FROM 
    schema_tablenames 
    JOIN (
        SELECT 
            table_schema, 
            table_name, 
            json_agg(
                json_build_object(
                    'column_name', column_name,
                    'data_type', data_type,
                    'field_type', 
                        CASE
                            WHEN data_type LIKE 'character varying%' THEN 'str'
                            WHEN data_type LIKE 'text%' THEN 'str'
                            WHEN data_type LIKE 'timestamp%' THEN 'str'
                            WHEN data_type LIKE 'inet%' THEN 'str'
                            WHEN data_type LIKE 'integer%' THEN 'int'
                            WHEN data_type LIKE 'bigint%' THEN 'int'
                            WHEN data_type LIKE 'oid%' THEN 'int'
                            WHEN data_type LIKE 'boolean%' THEN 'bool'
                            WHEN data_type LIKE 'numeric%' THEN 'float'
                            WHEN data_type LIKE 'double precision%' THEN 'float'
                            WHEN data_type LIKE 'ARRAY%' THEN 'list'
                            WHEN data_type LIKE 'json%' THEN '(dict or list)'
                            ELSE 'Any'
                        END
                )
            ) AS columns
        FROM 
            information_schema.columns 
        GROUP BY 
            table_schema, 
            table_name
    ) AS table_columns 
        ON schema_tablenames.table_schema = table_columns.table_schema 
            AND schema_tablenames.table_name = table_columns.table_name 
GROUP BY 
    schema_tablenames.table_schema
ORDER BY 
    schema_tablenames.table_schema