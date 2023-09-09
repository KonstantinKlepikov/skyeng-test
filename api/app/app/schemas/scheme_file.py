from pydantic import BaseModel, ConfigDict
from app.schemas.constraint import PydanticObjectId


class FileBase(BaseModel):
    user_id: PydanticObjectId

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123456789",
                    }
                }

class FileName(BaseModel):
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "my_file_name",
                    }
                }


class FileCheck(BaseModel):
    is_checked: bool = False
    is_email_sended: bool = False
    is_deleted_by_user: bool = False
    class Config:
        json_schema_extra = {
            "example": {
                "is_checked": False,
                "is_email_sended": False,
                "is_deleted_by_user": False,
                    }
                }


class File(FileBase, FileName, FileCheck):

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123456789",
                "name": "my_file_name",
                "is_checked": False,
                "is_email_sended": False,
                "is_deleted_by_user": False,
                    }
                }


class FileRaw(FileBase):
    file_id: PydanticObjectId
    raw: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123456789",
                "file_id": "123456789",
                "raw": "12345",
            }
        }


class Files(BaseModel):
    files: dict[PydanticObjectId, File]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra = {
            "example": {
                "files": {
                    "12345":
                        {
                    "user_id": "123456789",
                    "name": "my_file_name",
                    "is_checked": False,
                    "is_email_sended": False,
                    "is_deleted_by_user": False,
                        },
                    },
                }
            },
        )


class FilesRaw(BaseModel):
    files_raw: dict[PydanticObjectId, FileRaw]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra = {
            "example": {
                "files_raw": {
                    "12345":
                        {
                    "user_id": "123456789",
                    "file_id": "123456789",
                    "raw": "12345",
                        }
                    },
                }
            },
        )
