import argparse
from pydantic import BaseModel


class BaseArgsModel(BaseModel):
    @classmethod
    def parse_args(cls):
        parser = argparse.ArgumentParser()
        for field in cls.__fields__.values():
            type, help = field.outer_type_, f"{cls.__name__}.{field.name}"
            parser.add_argument(f"--{field.name}", type=type, help=help)
        parsed_args, _ = parser.parse_known_args()
        return cls(**vars(parsed_args))
