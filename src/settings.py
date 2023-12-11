from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", str_strip_whitespace=True, env_prefix="db_"
    )

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
        env_file=".env", str_strip_whitespace=True, env_prefix="auth_"
    )

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


db_settings = DatabaseSettings()
# print(db_settings)
auth_settings = AuthSettings()
# print(auth_settings)
