from typing import Optional, List, Union
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from app.schemas.model import Model
from app.schemas.status import Status
import enum

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
    status: Status
    model: Model
    name: str
    year: date
    sale_price: float
    rent_price: float
    description: str
    picture: Optional[str] = None
    created_at: datetime

class YachtListResponse(BaseModel):
    current_page: int = 0
    total_pages: int = 0
    yachts: List[Yacht]

class SortType(enum.Enum):
    price_asc = "price_asc"
    price_desc = "price_desc"
    available_for_rent = "available_for_rent"
    available_for_sale = "available_for_sale"

class YachtFilter(BaseModel):
    name: Optional[str] = ""
    model_id: Optional[str] = None
    page: Optional[int] = 1
    minLength: Optional[float] = 0
    maxLength: Optional[float] = 100
    minWidth: Optional[float] = 0
    maxWidth: Optional[float] = 100
    minPrice: Optional[float] = 0
    maxPrice: Optional[float] = 10**10
    sort_by: Optional[SortType] = "price_desc"
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
