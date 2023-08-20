from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.schemas import scheme_user
from app.crud import crud_user
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/user/login")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> scheme_user.User:
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

    user = await crud_user.users.get(token_data.email)

    if user is None:
        raise credentials_exception

    return scheme_user.User.model_validate(user.to_mongo().to_dict())
