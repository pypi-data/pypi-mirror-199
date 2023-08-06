from pydantic import BaseModel
from urllib.parse import urlparse
from dotenv import dotenv_values


class DatabaseURL(BaseModel):
    DATABASE_DRIVER: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str

    @property
    def dsn(self):
        dsn = f"{self.DATABASE_DRIVER}://"
        if self.DATABASE_USER and self.DATABASE_PASSWORD:
            dsn += f"{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@"
        dsn += self.DATABASE_HOST
        if self.DATABASE_PORT:
            dsn += f":{self.DATABASE_PORT}"
        dsn += f"/{self.DATABASE_NAME}"
        return dsn

    @classmethod
    def parse_dict(cls, __dict: dict):
        return cls(**{key: __dict.get(key) for key in cls.__fields__.keys()})

    @classmethod
    def parse_dotenv(cls, env_path: str):
        return cls.parse_dict(dict(dotenv_values(env_path).items()))

    @classmethod
    def parse_dsn(cls, dsn: str):
        parsed_url = urlparse(dsn)
        return cls(
            DATABASE_DRIVER=parsed_url.scheme,
            DATABASE_NAME=parsed_url.path[1:],
            DATABASE_USER=parsed_url.username,
            DATABASE_PASSWORD=parsed_url.password,
            DATABASE_HOST=parsed_url.hostname,
            DATABASE_PORT=str(parsed_url.port),
        )
