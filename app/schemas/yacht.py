from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class YachtBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class YachtCreate(YachtBase):
    status_id: int
    model_id: int
    name: str
    year: date
    sale_price: float
    rent_price: float
    description: str

class YachtUpdate(YachtBase):
    status_id: Optional[int] = None
    model_id: Optional[int] = None
    name: Optional[str] = None
    year: Optional[date] = None
    sale_price: Optional[float] = None
    rent_price: Optional[float] = None
    description: Optional[str] = None

class Yacht(YachtBase):
    id: int
    status_id: int
    model_id: int
    name: str
    year: date
    sale_price: float
    rent_price: float
    description: str
    picture: Optional[str] = None
    created_at: datetime
