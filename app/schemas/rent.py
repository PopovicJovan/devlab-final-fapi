from dataclasses import fields
from typing import Optional

from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, model_validator, field_validator
from datetime import date, datetime

from app.models import Yacht
from app.schemas.yacht import Yacht as YachtSchema
from app.views.yacht import YachtView


class RentBase(BaseModel):
    yacht: YachtSchema
    start_date: date
    end_date: date
    @model_validator(mode='after')
    def check_end_start_date(self) -> Self:
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')
        return self

    @field_validator("yacht", mode="after")
    def encode_yacht_picture_to_base64(cls, value: Yacht) -> Yacht:
        if value.picture:
            picture = YachtView.get_yacht_photo(value)
            value.picture = f"data:image/jpeg;base64,{picture}" if picture else None
        return value
    model_config = ConfigDict(from_attributes=True)


class RentCreate(RentBase):
    #user_id:int
    #total_price: float
    yacht: Optional[YachtSchema] = None
    yacht_id : int

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end_date <= datetime.now().date():
            raise ValueError('end_date must be after current date')
        if self.start_date <= datetime.now().date():
            raise ValueError('start_date must be after current date')
        return self



class Rent(RentBase):
    id: int
    user_id: int
    total_price: float
    created_at: datetime

class RentDates(BaseModel):
    start_date: date
    end_date: date
    model_config = ConfigDict(from_attributes=True)
