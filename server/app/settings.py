from pathlib import Path
from typing import List

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    DirectoryPath,
    PostgresDsn,
    SecretStr,
    validator,
)

from app.enums.logenums import LogLevel


class Settings(BaseSettings):

    APP_DIR: DirectoryPath = Path(__file__).resolve().parent
    STATIC_DIR: DirectoryPath = APP_DIR / "static"
    EMAIL_TEMPLATES_DIR: DirectoryPath = STATIC_DIR / "email-templates" / "html"

    PROJECT_NAME: str

    SERVER_HOST: str
    CORS_WHITELIST: List[AnyHttpUrl] = []

    FASTAPI_ENV: str
    DEBUG: bool = False
    LOG_LEVEL: LogLevel = LogLevel.debug

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    USERS_OPEN_REGISTRATION: bool

    SECRET_KEY: SecretStr
    JWT_AUTH_LIFETIME_SECONDS: int = 60 * 60 * 24 * 7  # 7 days
    JWT_EMAIL_LIFETIME_SECONDS: int = 60 * 60 * 1  # 1 hour

    SMTP_USER: str
    SMTP_PASSWORD: SecretStr
    SMTP_TLS: bool
    SMTP_SSL: bool
    SMTP_HOST: str
    SMTP_PORT: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: PostgresDsn = None

    @validator("POSTGRES_URL", pre=True)
    def build_pgdsn(cls, v, values):
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"].get_secret_value(),
            host=values["POSTGRES_HOST"],
            port=str(values["POSTGRES_PORT"]),
            path="/" + values["POSTGRES_DB"],
        )


settings = Settings()
