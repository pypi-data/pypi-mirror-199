import tomllib
from typing import Literal, Optional, Self
from pydantic import BaseModel, Field
from datetime import timedelta

_DEFAULT_TIMEOUT = timedelta(seconds=1, milliseconds=100)
_DEFAULT_COOKIE_TTL = timedelta(days=90)


class SessionConfig(BaseModel):
    cookie: str = "_gassio_session_id"
    ttl: timedelta = _DEFAULT_COOKIE_TTL


class DatabaseConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = Field(3000, gt=0, lt=65536)
    dbname: str = "glassiodb"
    timeout: timedelta = _DEFAULT_TIMEOUT

    @property
    def uri(self) -> str:
        return f"mongodb://{self.host}:{self.port}/{self.dbname}"


class LogConfig(BaseModel):
    level: Literal["critical", "error", "warning", "info", "debug"] = "debug"
    filename: Optional[str] = None
    stdout: bool = True


class OAuthConfig(BaseModel):
    id: str
    secret: str
    authorize_url: str


class WebConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = Field(3000, gt=0, lt=65536)


class GeneralConfig(BaseModel):
    documents_per_page: int = 20
    environment: Literal["development", "testing", "staging", "production"] = "development"
    enable_passwords: bool = True


class BaseConfig(BaseModel):
    session: SessionConfig = Field(default_factory=SessionConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LogConfig = Field(default_factory=LogConfig)
    oauth: Optional[OAuthConfig] = Field(None)
    web: WebConfig = Field(default_factory=WebConfig)
    general: GeneralConfig = Field(default_factory=GeneralConfig)

    @classmethod
    def parse(cls, filename) -> Self:
        with open(filename, "rb") as f:
            config = tomllib.load(f)
        return cls(**config)
