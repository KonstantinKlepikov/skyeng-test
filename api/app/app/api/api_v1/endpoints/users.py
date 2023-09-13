from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pymongo.client_session import ClientSession
from pymongo.errors import DuplicateKeyError
from app.schemas import scheme_user
from app.crud.crud_user import users
from app.core import security
from app.db.init_db import get_session
from app.config import settings


router = APIRouter()


@router.post(
    '/create',
    status_code=status.HTTP_201_CREATED,
    responses=settings.AUTHENTICATE_RESPONSE_ERRORS,
    summary='Create user',
    response_description="""Created.""",
        )
async def create_user(
    user: scheme_user.User,
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Create user

    - **password** - string with at least 8 characters
    - **email** - valid email string
    """
    obj_in = scheme_user.UserInDb(
        email=user.email,
        hashed_password=security.get_password_hash(user.password)
            )
    try:
        # if email not exist -> True
        email_not_exist = await users.create(db, obj_in)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail='Email is exist in data base.'
                )

    if not email_not_exist:
        raise HTTPException(
            status_code=409,
            detail='Email is exist in data base.'
                )


@router.post(
    "/login",
    response_model=scheme_user.Token,
    status_code=status.HTTP_200_OK,
    responses=settings.AUTHENTICATE_RESPONSE_ERRORS,
    summary='Authenticate user',
    response_description="OK. As response you receive access token. "
                         "Use it for bearer autentication."
        )
async def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: ClientSession = Depends(get_session),
        ) -> dict[str, str]:
    """Send for autorization:

    - **email** as login
    - **password**
    """
    db_user: scheme_user.UserInDb = await users.get(
        db,
        {"email": user.username}
            )

    if not db_user or not security.verify_password(
        user.password, db_user["hashed_password"]
            ):
        raise HTTPException(
            status_code=400,
            detail='Wrong login or password or user not exist.'
                )

    else:
        return {
            'access_token': security.create_access_token(
                subject=user.username
                    ),
            "token_type": "bearer"
                }
