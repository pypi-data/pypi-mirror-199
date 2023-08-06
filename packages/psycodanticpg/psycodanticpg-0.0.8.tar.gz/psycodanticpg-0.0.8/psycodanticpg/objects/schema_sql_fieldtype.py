import uuid
import datetime
from typing import Any
from decimal import Decimal
from pydantic import BaseModel
from pydantic import BaseConfig
from psycopg2.extras import Json


class SchemaSQLFieldType(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    name: str
    field_type: Any

    @property
    def sql_type(self) -> str:
        fieldtype = self.field_type
        try:
            typename = fieldtype.__name__
        except:
            typename = ""
        typename_lower = typename.lower()
        for type_prefix, result_type in (
            ("int", "int"),
            ("float", "real"),
            ("str", "varchar"),
            ("bool", "boolean"),
            ("dict", "jsonb"),
        ):
            if typename_lower.startswith(type_prefix):
                result = result_type
                break
        else:
            for match_type, result_type in (
                (int, "int"),
                (float, "real"),
                (str, "varchar"),
                (bool, "boolean"),
                (datetime.date, "date"),
                (datetime.time, "time"),
                (datetime.datetime, "timestamp"),
                (uuid.UUID, "uuid"),
                (bytes, "bytea"),
                (Decimal, "numeric"),
                (dict, "jsonb"),
                (list, "jsonb"),
            ):
                if fieldtype == match_type:
                    result = result_type
                    break
            else:
                raise ValueError(f"Unsupported Pydantic type: {fieldtype}")
        return result

    def from_obj(self, obj):
        result = getattr(obj, self.name)
        if self.sql_type == "jsonb":
            result = Json(result)
        return result
