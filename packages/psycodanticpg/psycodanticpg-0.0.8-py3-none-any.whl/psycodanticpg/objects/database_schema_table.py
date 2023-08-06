from typing import List
from pydantic import BaseModel
from .database_schema_column import DatabaseSchemaColumn


class DatabaseSchemaTable(BaseModel):
    table_name: str
    columns: List[DatabaseSchemaColumn]
