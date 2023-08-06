from typing import TypeVar
from pydantic import BaseModel

SomeSchema = TypeVar("SomeSchema", bound=BaseModel)
