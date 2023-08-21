import toml
from typing import Type
from pydantic import  SecretStr, RedisDsn
from pydantic.networks import AnyUrl
from pydantic_settings import BaseSettings
from app.schemas import scheme_error


poetry_data = toml.load('pyproject.toml')['tool']['poetry']
ErrorType = dict[int, dict[str, Type[scheme_error.HttpErrorMessage]]]


class Settings(BaseSettings):
    # api vars
    API_V1: str = "/api/v1"

    # db settings
    MONGODB_URL: SecretStr | None = None
    DB_NAME: str | None = None
    CELERY_BROKER_URL: RedisDsn | None = None
    TOKEN_EXPIRES_MINUTES: int | None = None
    SECRET_KEY: SecretStr | None = None
    ALGORITHM: str | None = None

    # open-api settings
    title: str = poetry_data['name']
    descriprion: str = poetry_data['description']
    version: str = poetry_data['version']
    openapi_tags: list = [
        {
            "name": "users",
            "description": "Users api",
        },
    ]

    # open-api errors
    AUTHENTICATE_RESPONSE_ERRORS: ErrorType = {
        400: {'model': scheme_error.HttpError400},
        422: {'model': scheme_error.HttpError422}
            }
    ACCESS_ERRORS: ErrorType = {
        401: {'model': scheme_error.HttpError401},
            }


settings = Settings()
