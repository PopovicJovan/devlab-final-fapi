from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class BaseClass(BaseModel):
    username: str
    password: str


class Register(BaseClass):
    username: Annotated[str, Field(..., min_length=2, max_length=16)]
    password: Annotated[str, Field(..., min_length=8)]
    email: EmailStr


class Login(BaseClass):
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    model_config = ConfigDict(from_attributes=True)
