from pydantic import BaseModel, validator
from pydantic.networks import EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token":
                    "$2b$12$sifRrf5m7GM0hhFAF7BQ0.dIokOEZkfYOawlal8Jp/GeWh/4zn8la",
                    "token_type": "bearer",
            }
        }

class TokenData(BaseModel):
    email: EmailStr | None = None

    class Config:
        schema_extra = {
            "example": {
                "email": "example@example.com",
            }
        }


class UserBase(BaseModel):
    email: EmailStr

    class Config:
        schema_extra = {
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
        schema_extra = {
            "example": {
                "password": "1jkR3Zt8",
            }
        }


class User(UserBase, UserPassword):
    pass

    class Config:
        schema_extra = {
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
        schema_extra = {
            "example": {
                "email": "example@example.com",
                "hashed_password":
                    "$2b$12$sifRrf5m7GM0hhFAF7BQ0.dIokOEZkfYOawlal8Jp/GeWh/4zn8la",
            }
        }
