import json
from pydantic import BaseModel
from .database_schema import DatabaseSchema


class DatabaseSchemas(BaseModel):
    schemas: dict[str, DatabaseSchema]

    @classmethod
    def parse_orm(cls, raw):
        schemas = raw
        if schemas is None:
            default_schema_names = ("public",)
            default_schemas = [
                DatabaseSchema(schema_name=schema_name, tables=[])
                for schema_name in default_schema_names
            ]
            schemas = {schema.schema_name: schema for schema in default_schemas}
            schemas = cls(schemas=schemas)
        else:
            schemas = schemas[0]
            if schemas is not None:
                data = json.dumps(dict(schemas=schemas))
            schemas = cls.parse_raw(data, content_type="json")
        return schemas

    def public(self) -> DatabaseSchema:
        return self.schemas["public"]
