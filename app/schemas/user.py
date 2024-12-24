from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.schemas.sale import Sale

class BaseClass(BaseModel):
    pass

class User(BaseModel):
    id: int
    email: str
    username: str
    picture: Optional[str] = None
    sales: List[Sale]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
