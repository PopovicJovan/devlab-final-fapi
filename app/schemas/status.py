from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional


class StatusEnum(Enum):
    RENTED = "rented"
    SOLD = "sold"
    AVAILABLE_FOR_RENT = "available for rent"
    AVAILABLE_FOR_SELL = "available for sell"
    AVAILABLE_FOR_RENT_SALE = "available for rent and sale"
    UNAVAILABLE = "unavailable"


class StatusBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StatusCreateUpdate(StatusBase):
    name: StatusEnum
    description: Optional[str] = None


class Status(StatusBase):
    id: int
    name: StatusEnum
    description: Optional[str] = None


