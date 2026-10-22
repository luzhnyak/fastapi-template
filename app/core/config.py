from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )


class DBSettings(EnvSettings):
    SQLITE_DB_PATH: str = "db.sqlite3"

    @property
    def DATABASE_URL(self) -> str:
        path = Path(self.SQLITE_DB_PATH).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return f"sqlite+aiosqlite:///{path}"


class AppSettings(EnvSettings):
    HOST: str = "127.0.0.1"
    PORT: int = Field(default=8000, ge=1, le=65535)
    RELOAD: bool = False
    SECRET_KEY: str = Field(min_length=32, repr=False)
    ALGORITHM: Literal["HS256"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=30, gt=0)
    BASE_URL: str = "http://localhost:8000"
    BASE_URL_NEXT: str = "http://localhost:3000"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    COOKIE_SECURE: bool = True
    INIT_DB: bool = True
    OAUTH_CLIENT_ID: str | None = None
    OAUTH_SECRET: str | None = Field(default=None, repr=False)
    OAUTH_REDIRECT_URI: str | None = None
    APP_FOLDER: str = str(PROJECT_ROOT)

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret(cls, value: str) -> str:
        if len(value.strip()) < 32:
            raise ValueError("Generate SECRET_KEY with secrets.token_hex(32)")
        return value

    @property
    def IMAGE_FOLDER(self) -> str:
        return str(Path(self.APP_FOLDER) / "static" / "img")


class Settings(EnvSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    db: DBSettings = Field(default_factory=DBSettings)


settings = Settings()
