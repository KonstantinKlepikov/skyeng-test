from pydantic import BaseModel, ConfigDict
from app.schemas.constraint import PydanticObjectId


class FileBase(BaseModel):
    name: str
    raw: bytes

    class Config:
        json_schema_extra = {
            "example": {
                "name": "my_file_name",
                "raw": b"12345",
            }
        }


class FileInDb(FileBase):
    user_id: PydanticObjectId
    is_checked: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra = {
            "example": {
                "name": "my_file_name",
                "raw": b"12345",
                "user_id": "123456789",
                "is_checked": False,
                }
            },
        )


class FilesInDb(BaseModel):
    files_ids: list[PydanticObjectId]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra = {
            "example": {
                "files_ids": ["123456789"],
                    }
                },
            )
