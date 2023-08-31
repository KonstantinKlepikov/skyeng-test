import os
import bson
from bson.errors import InvalidId
import pickle
from typing import Any
from fastapi import (
    APIRouter,
    UploadFile,
    Depends,
    status,
    HTTPException,
        )
from fastapi.responses import Response
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
    response_description="""Files ids owned by user.""",
        )
async def get_files(
    user: dict[str, Any] = Depends(security_user.get_current_user),
    db: ClientSession = Depends(get_session),
    lenght: int = 100,
        ) -> None:
    """Get files ids owned by user
    """
    f = await files.get_many(
        db,
        q={"user_id": str(user['_id'])},
        lenght=lenght
            )
    return scheme_file.FilesInDb(
        files={str(i['_id']): i['name'] for i in f}
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
    obj_in = scheme_file.FileInDb(
        raw=bson.Binary(pickle.dumps(file.file)),
        name=name,
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
    try:
        f = await files.get(db, {'_id': bson.ObjectId(id)})
    except InvalidId:
        raise HTTPException(
            status_code=404,
            detail=f'Wrong file {id=}.'
                )

    if f and f['user_id'] == str(user['_id']):
        return Response(
            content=f['raw'],
            media_type='text/x-python',
            headers = {
                'Content-Disposition': f'''attachment; filename="{f['name']}.py"'''
                }
            )
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
        result = await files.delete(
            db,
            q={'_id': bson.ObjectId(id), 'user_id': str(user['_id'])},
                )
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f'File with {id=} not found.'
                    )
    except InvalidId:
        raise HTTPException(
            status_code=404,
            detail=f'Wrong file {id=}.'
                )


@router.put(
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
        name, ex = os.path.splitext(file.filename)
        if ex != '.py':
            raise HTTPException(
                status_code=409,
                detail='Wrong file extention.'
                    )
        obj_in = scheme_file.FileInDb(
            raw=bson.Binary(pickle.dumps(file.file)),
            name=name,
            user_id=str(user['_id']),
            )
        result = await files.replace(
            db,
            q={'_id': bson.ObjectId(id), 'user_id': str(user['_id'])},
            obj_in=obj_in,
                )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail=f'File with {id=} not found.'
                    )
    except InvalidId:
        raise HTTPException(
            status_code=404,
            detail=f'Wrong file {id=}.'
                )
