from pydantic import BaseModel, validator
from pydantic.networks import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token":
                    "$somehash",
                    "token_type": "bearer",
            }
        }


class TokenData(BaseModel):
    email: EmailStr | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@example.com",
            }
        }


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@example.com",
            }
        }


class UserPassword(BaseModel):
    password: str

    @validator('password')
    def passwords_must_have_eight_or_more_characters(cls, v):
        if 50 < len(v) < 8:
            raise ValueError('Unsafe password: use at least 8 characters')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "password": "1jkR3Zt8",
            }
        }


class User(UserBase, UserPassword):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "password": "1jkR3Zt8",
                "email": "example@example.com",
            }
        }


class UserInDb(UserBase):
    """User in bd
    """
    hashed_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@example.com",
                "hashed_password":
                    "$somehash",
            }
        }
