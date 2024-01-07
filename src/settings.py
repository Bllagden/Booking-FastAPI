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
    def url(self):
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


db_settings = DatabaseSettings()
auth_settings = AuthSettings()
app_settings = AppSettings()

# print(db_settings)
# print(auth_settings)
# print(app_settings.ALLOW_ORIGINS)
