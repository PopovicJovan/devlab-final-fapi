from datetime import datetime

from pydantic import BaseModel


class BaseClass(BaseModel):
    pass

class User(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime