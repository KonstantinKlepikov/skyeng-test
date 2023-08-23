from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pymongo.client_session import ClientSession
from jose import jwt, JWTError
from app.schemas import scheme_user
from app.crud import crud_user
from app.db.init_db import get_session
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/users/login")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    db: ClientSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
        ) -> dict[str, Any]:
    """Get current verified user
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY.get_secret_value(),
            algorithms=[settings.ALGORITHM]
                )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = scheme_user.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = await crud_user.users.get(db, {"email": token_data.email})

    if not user:
        raise credentials_exception

    return user
