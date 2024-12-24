from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class RentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class RentCreate(RentBase):
    yacht_id: int
    #user_id:int
    start_date: date
    end_date: date
    #total_price: float

class RentResponse(RentBase):
    id: int
    yacht_id: int
    user_id: int
    start_date: date
    end_date: date
    total_price: float
    created_at: datetime