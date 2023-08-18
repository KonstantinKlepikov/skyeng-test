from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import create_collections
from app.config import settings
from app.api.api_v1.api import api_router


app = FastAPI(
    title=settings.title,
    openapi_url=f"{settings.API_V1}/openapi.json",
    description=settings.descriprion,
    version=settings.version,
    openapi_tags=settings.openapi_tags,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    on_startup=[create_collections],
    on_shutdown=[],
        )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_V1)
