# import functools
from typing import Literal, TypeVar

# import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

TSettings = TypeVar("TSettings", bound=BaseSettings)


def get_settings(cls: type[TSettings]) -> TSettings:
    # dotenv.load_dotenv()
    return cls()


# get_settings = functools.lru_cache(get_settings)  # Mypy moment


class DatabaseSettings(BaseSettings):
    """При тестировании '.env.dev' меняется на '.env.test' библиотекой pytest-dotenv.
    При запуске Docker-Compose '.env.dev' меняется на '.env.prod' докером."""

    model_config = SettingsConfigDict(
        env_file=".env.dev", str_strip_whitespace=True, env_prefix="db_"
    )

    mode: Literal["DEV", "TEST", "PROD"]
    driver: str
    host: str
    port: int
    user: str
    password: str
    name: str

    echo: bool = False

    @property
    def url(self):
        """
        Строка подключения к БД (адрес). Указывает SQLAlchemy, как подключиться к БД.
        asyncpg (драйвер БД) - API для асинхронного взаимодействия с postgresql.
        """
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="auth_")
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class AppSettings(BaseSettings):
    """allow_origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        https://api.mysite.com,
    ]"""

    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="app_")
    allow_origins: list[str]


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="redis_")

    host: str
    port: str


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="smtp_")

    host: str
    port: str
    user: str
    password: str


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(str_strip_whitespace=True, env_prefix="log_")
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
