from fastapi import APIRouter
from app.api.api_v1.endpoints import users, files


api_router = APIRouter()


api_router.include_router(
    users.router, prefix="/users", tags=['users', ],
        )
api_router.include_router(
    files.router, prefix="/files", tags=['files', ]
        )
