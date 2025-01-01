from __future__ import annotations
from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel, field_validator
from app.schemas.yacht import Yacht
from app.views.yacht import YachtView


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

    @field_validator("yacht", mode="after")
    def encode_yacht_picture_to_base64(cls, value: Yacht) -> Yacht:
        if value.picture:
            picture = YachtView.get_yacht_photo(value)
            value.picture = f"data:image/jpeg;base64,{picture}" if picture else None
        return value
from app.schemas.user import User
User.model_rebuild()
