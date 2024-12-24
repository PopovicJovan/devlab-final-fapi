from __future__ import annotations
from datetime import datetime
from pydantic import ConfigDict, BaseModel
from app.schemas.yacht import Yacht

class SaleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SaleCreate(SaleBase):
    user_id: int
    yacht_id: int


class Sale(SaleBase):
    id: int
    user: User
    yacht: Yacht
    created_at: datetime


from app.schemas.user import User
User.model_rebuild()
