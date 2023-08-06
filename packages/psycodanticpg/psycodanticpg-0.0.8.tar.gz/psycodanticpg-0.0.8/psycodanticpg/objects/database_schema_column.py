from pydantic import BaseModel


class DatabaseSchemaColumn(BaseModel):
    column_name: str
    data_type: str
    field_type: str
