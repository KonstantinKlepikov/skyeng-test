import os
import bson
import pickle
from typing import Any
from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    status,
    HTTPException
        )
from pymongo.client_session import ClientSession
from app.db.init_db import get_session
from app.schemas import scheme_file
from app.crud.crud_file import files
from app.core import security_user
from app.config import settings


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses=settings.FILE_ERRORS,
    summary='Files ids owned by user',
    response_description="""Files id's owned by user.""",
        )
async def get_files(
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Get files owned by user
    """
    # TODO:


@router.post(
    "/file/",
    status_code=status.HTTP_201_CREATED,
    responses=settings.FILE_ERRORS,
    summary='File upload',
    response_description="""Uploaded.""",
        )
async def create_file(
    file: UploadFile,
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Upload new file, check is .py and save it in db
    """
    _, ex = os.path.splitext(file.filename)
    if ex != '.py':
        raise HTTPException(
            status_code=409,
            detail='Wrong file extention.'
                )
    obj_in = scheme_file.FileInDb(
        raw=bson.Binary(pickle.dumps(file.file)),
        user_id=str(user['_id']),
            )
    await files.create(db, obj_in)


@router.get(
    "/file/",
    status_code=status.HTTP_200_OK,
    responses=settings.FILE_ERRORS,
    summary='File download',
    response_description="""File binary.""",
        )
async def get_file(
    id: str,
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Get file binary from db
    """
    # TODO:


@router.delete(
    "/file/",
    status_code=status.HTTP_200_OK,
    responses=settings.FILE_ERRORS,
    summary='File delete',
    response_description="""Deleted.""",
        )
async def delete_file(
    id: str,
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Delete file from db
    """
    # TODO:


@router.put(
    "/file/",
    status_code=status.HTTP_201_CREATED,
    responses=settings.FILE_ERRORS,
    summary='File delete',
    response_description="""Updated.""",
        )
async def update_file(
    id: str,
    file: UploadFile,
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Update file in db
    """
    # TODO:

