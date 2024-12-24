from datetime import datetime

from pydantic import ConfigDict, BaseModel


class SaleBase(BaseModel):
    user_id: int
    yacht_id: int

    model_config = ConfigDict(from_attributes=True)


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: int
    created_at: datetime
