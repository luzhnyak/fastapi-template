import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    SQLITE_DB_PATH: str = "db.sqlite3"

    @property
    def DATABASE_URL(self) -> str:
        db_path = Path(self.SQLITE_DB_PATH).absolute()
        return f"sqlite+aiosqlite:///{db_path}"

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
    db: DBSettings = DBSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
