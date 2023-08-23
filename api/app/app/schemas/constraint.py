from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator
from enum import Enum


class BaseEnum(Enum):
    """Base class for enumeration
    """
    @classmethod
    def has_value(cls, value: str | int) -> bool:
        return value in cls._value2member_map_

    @classmethod
    def get_values(cls) -> list[str | int]:
        return [e.value for e in cls]

    @classmethod
    def get_names(cls) -> list[Enum]:
        return [e for e in cls]


class BaseStrEnum(str, BaseEnum):
    """Base class for enumeration
    """


class Collections(BaseStrEnum):
    USERS = 'users'
    FILES = 'files'


def check_object_id(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value


PydanticObjectId = Annotated[str, AfterValidator(check_object_id)]

