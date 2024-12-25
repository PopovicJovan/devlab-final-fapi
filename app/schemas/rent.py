from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, model_validator
from datetime import date, datetime

class RentBase(BaseModel):
    yacht_id: int
    start_date: date
    end_date: date
    @model_validator(mode='after')
    def check_end_start_date(self) -> Self:
        if self.end_date <= self.start_date:
            raise ValueError('end_date must be after start_date')
        return self
    model_config = ConfigDict(from_attributes=True)


class RentCreate(RentBase):
    #user_id:int
    #total_price: float

    @model_validator(mode='after')
    def check_dates(self) -> Self:
        if self.end_date <= datetime.date(datetime.now()):
            raise ValueError('end_date must be after current date')
        if self.start_date <= datetime.date(datetime.now()):
            raise ValueError('start_date must be after current date')
        return self

class Rent(RentBase):
    id: int
    user_id: int
    total_price: float
    created_at: datetime



