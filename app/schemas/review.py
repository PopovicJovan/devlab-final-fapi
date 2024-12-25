from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
class ReviewBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(ReviewBase):
    rent_id:int
    rate: int = Field(int, ge=1, le=5)
    comment:str


class ReviewResponse(ReviewBase):
    id:int
    rent_id:int
    rate:int
    comment:str
    created_at:datetime