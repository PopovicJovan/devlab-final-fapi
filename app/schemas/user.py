from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class BaseClass(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: int
    email: str
    username: str
    picture: Optional[str] = None
    created_at: datetime

class UserWithSales(User):
    sales: List[Sale]

from app.schemas.sale import Sale
Sale.model_rebuild()