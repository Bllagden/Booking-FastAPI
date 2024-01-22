from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env", str_strip_whitespace=True, env_prefix="db_"
    )
    MODE: Literal["DEV", "TEST", "PROD"]

    DRIVER: str
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    @property
    def URL(self):
        """
        Строка подключения к БД (адрес). Указывает SQLAlchemy, как подключиться к БД.
        asyncpg (драйвер БД) - API для асинхронного взаимодействия с postgresql.
        """
        return f"{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env", str_strip_whitespace=True, env_prefix="auth_"
    )
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


class AppSettings(BaseSettings):
    """allow_origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        https://api.mysite.com,
    ]"""

    model_config = SettingsConfigDict(
        env_file=".dev.env", str_strip_whitespace=True, env_prefix="app_"
    )
    ALLOW_ORIGINS: list[str]


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env", str_strip_whitespace=True, env_prefix="redis_"
    )
    HOST: str
    PORT: str


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env", str_strip_whitespace=True, env_prefix="smtp_"
    )
    HOST: str
    PORT: str
    USER: str
    PASSWORD: str


class LogSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".dev.env", str_strip_whitespace=True, env_prefix="log_"
    )
    LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


db_settings = DatabaseSettings()
auth_settings = AuthSettings()
app_settings = AppSettings()
redis_settings = RedisSettings()
smtp_settings = SMTPSettings()
log_settings = LogSettings()

# print(db_settings)
# print(auth_settings)
# print(app_settings.ALLOW_ORIGINS)
# print(redis_settings)
# print(smtp_settings)
# print(log_settings)
