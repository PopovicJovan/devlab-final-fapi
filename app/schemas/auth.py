from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class BaseClass(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(..., min_length=8)]


class Register(BaseClass):
    username: Annotated[str, Field(..., min_length=2, max_length=16)]


class Login(BaseClass):
    pass

