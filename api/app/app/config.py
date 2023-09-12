import toml
from typing import Type
from pydantic import  SecretStr, RedisDsn, EmailStr
from pydantic_settings import BaseSettings
from app.schemas import scheme_error


poetry_data = toml.load('pyproject.toml')['tool']['poetry']
ErrorType = dict[int, dict[str, Type[scheme_error.HttpErrorMessage]]]


class Settings(BaseSettings):
    # api vars
    API_V1: str = "/api/v1"

    # mongo settings
    MONGODB_URL: SecretStr | None = None
    DB_NAME: str | None = None
    TOKEN_EXPIRES_MINUTES: int | None = None
    SECRET_KEY: SecretStr | None = None
    ALGORITHM: str | None = None

    # celery
    CELERY_BROKER_URL: RedisDsn | None = None
    TIME_TO_CHECK: float = 30.0

    # email settings
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: SecretStr | None = None
    MAIL_FROM: EmailStr | None = None
    MAIL_PORT: int = 587
    MAIL_SERVER: str | None = None  # FIXME: a server uri str
    MAIL_FROM_NAME: str | None = None
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # open-api settings
    title: str = poetry_data['name']
    descriprion: str = poetry_data['description']
    version: str = poetry_data['version']
    openapi_tags: list = [
        {
            "name": "users",
            "description": "Users api",
        },
        {
            "name": "files",
            "description": "Files api",
        },
    ]

    # open-api errors
    AUTHENTICATE_RESPONSE_ERRORS: ErrorType = {
        400: {'model': scheme_error.HttpError400},
        409: {'model': scheme_error.HttpError409}
            }
    ACCESS_ERRORS: ErrorType = {
        401: {'model': scheme_error.HttpError401},
            }
    FILE_ERRORS: ErrorType = {
        401: {'model': scheme_error.HttpError401},
        409: {'model': scheme_error.HttpError409},
            }


settings = Settings()
