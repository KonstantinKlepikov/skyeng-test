import os
import bson
from bson.errors import InvalidId
from typing import Any
from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    status,
    HTTPException,
        )
from fastapi.responses import PlainTextResponse
from pymongo.client_session import ClientSession
from app.db.init_db import get_session
from app.schemas import scheme_file
from app.crud.crud_file import files, files_raw
from app.core import security_user
from app.config import settings


router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses=settings.FILE_ERRORS,
    summary='Files wned by user data',
    response_description="""Files owned by user.""",
        )
async def get_files(
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
    lenght: int = 100,
        ) -> None:
    """Get files owned by user data (without raw file text)
    """
    # TODO: sorted by name lex
    f = await files.get_many(
        db,
        q={"user_id": str(user['_id']), 'is_deleted_by_user': False},
        lenght=lenght
            )
    return scheme_file.Files(
        files={
            str(i['_id']): scheme_file.File(**i)
            for i in f
            # if not i['is_deleted_by_user']
            }
        )


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
    name, ex = os.path.splitext(file.filename)
    if ex != '.py':
        raise HTTPException(
            status_code=409,
            detail='Wrong file extention.'
                )
    obj_in = scheme_file.File(
        name=name,
        user_id=str(user['_id']),
            )
    # FIXME: this needs a transaction ->
    result = await files.create(db, obj_in)
    obj_in = scheme_file.FileRaw(
        raw=file.file.read().decode(),
        file_id=str(result.inserted_id),
        user_id=str(user['_id']),
            )
    await files_raw.create(db, obj_in)
    # <-


@router.get(
    "/file/",
    status_code=status.HTTP_200_OK,
    responses=settings.FILE_ERRORS,
    summary='File download',
    response_description="""File as text.""",
    response_class=PlainTextResponse,
        )
async def get_file(
    id: str,
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Get file text from db
    """
    try:
        f = await files_raw.get(db, {'file_id': id})
    except InvalidId:
        raise HTTPException(
            status_code=404,
            detail=f'Wrong file {id=}.'
                )

    if f and f['user_id'] == str(user['_id']):
            return f['raw']
    else:
        raise HTTPException(
            status_code=404,
            detail=f'File with {id=} not found.'
                )


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
    try:
        # FIXME: this needs a transaction ->
        result = await files.delete(
            db,
            q={'_id': bson.ObjectId(id), 'user_id': str(user['_id'])},
                )
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f'File with {id=} not found.'
                    )
        await files_raw.delete(
            db,
            q={'file_id': id, 'user_id': str(user['_id'])},
                )
        # <-

    except InvalidId:
        raise HTTPException(
            status_code=404,
            detail=f'Wrong file {id=}.'
                )


@router.put(
    "/file/",
    status_code=status.HTTP_200_OK,
    responses=settings.FILE_ERRORS,
    summary='Mark file as deleted',
    response_description="""Marked.""",
        )
async def delete_file(
    id: str,
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
        ) -> None:
    """Mark file as deleted
    """
    try:
        obj_in = scheme_file.FileCheck(is_deleted_by_user=True).model_dump()
        result = await files.update(
            db,
            q={'_id': bson.ObjectId(id), 'user_id': str(user['_id'])},
            obj_in=obj_in,
                )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f'File with {id=} not found.'
                    )
    except InvalidId:
        raise HTTPException(
            status_code=404,
            detail=f'Wrong file {id=}.'
                )


@router.patch(
    "/file/",
    status_code=status.HTTP_201_CREATED,
    responses=settings.FILE_ERRORS,
    summary='File update',
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
    try:
        _, ex = os.path.splitext(file.filename)
        if ex != '.py':
            raise HTTPException(
                status_code=409,
                detail='Wrong file extention.'
                    )

        # TODO: this needs a transaction ->
        obj_in = scheme_file.FileRaw(
            raw=file.file.read().decode(),
            file_id=id,
            user_id=str(user['_id']),
                ).model_dump()

        result = await files_raw.replace(
            db,
            q={'file_id': id, 'user_id': str(user['_id'])},
            obj_in=obj_in,
                )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f'File with {id=} not found.'
                    )

        obj_in = scheme_file.FileCheck().model_dump()
        result = await files.update(
            db,
            q={'_id': bson.ObjectId(id), 'user_id': str(user['_id'])},
            obj_in=obj_in,
                )
        # < -

    except InvalidId:
        raise HTTPException(
            status_code=404,
            detail=f'Wrong file {id=}.'
                )
