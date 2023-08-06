from typing import List
from pydantic import BaseModel
from .database_schema_table import DatabaseSchemaTable


class DatabaseSchema(BaseModel):
    schema_name: str
    tables: List[DatabaseSchemaTable]
