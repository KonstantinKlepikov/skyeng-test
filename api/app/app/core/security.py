from datetime import datetime, timedelta
from typing import Any
from jose import jwt
from passlib.context import CryptContext
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: str | Any, expires_delta: timedelta = None
        ) -> str:
    """Create access token with defined expiration time

    Args:
        subject (Union[str, Any]): subject data
        expires_delta (timedelta, optional): how long token leave.
                                             Defaults to None.

    Returns:
        str: JWT token
    """
    expire = None
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    elif settings.TOKEN_EXPIRES_MINUTES:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.TOKEN_EXPIRES_MINUTES
        )

    if expire:
        to_encode = {"exp": expire, "sub": str(subject)}
    else:
        to_encode = {"sub": str(subject)}

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY.get_secret_value(),
        algorithm=settings.ALGORITHM
            )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compoare the password with hashed password

    Args:
        plain_password (str): -
        hashed_password (str): -

    Returns:
        bool: result of check
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    """Get hsash of password

    Args:
        plain_password (str): -

    Returns:
        str: hashed password
    """
    return pwd_context.hash(plain_password)
