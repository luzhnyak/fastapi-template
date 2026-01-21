import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str = "localhost"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class AppSettings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8095
    RELOAD: bool = False
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    BASE_URL: str
    BASE_URL_NEXT: str
    APP_FOLDER: str = os.path.dirname(os.path.abspath(__file__))

    @property
    def IMAGE_FOLDER(self) -> str:
        return os.path.join(self.APP_FOLDER, "static", "img")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    postgres: PostgresSettings = PostgresSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
