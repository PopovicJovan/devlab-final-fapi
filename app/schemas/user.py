from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseClass(BaseModel):
    pass

class User(BaseModel):
    id: int
    email: str
    username: str
    picture: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
