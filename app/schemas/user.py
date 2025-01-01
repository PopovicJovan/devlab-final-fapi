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
    admin: bool
    created_at: datetime

class UserWithSalesAndRents(User):
    sales: List[Sale] = []
    rents: List[Rent] = []



from app.schemas.sale import Sale
from app.schemas.rent import Rent
Sale.model_rebuild()
Rent.model_rebuild()
