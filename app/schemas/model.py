from pydantic import BaseModel, ConfigDict
from typing import Optional

class ModelBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ModelCreate(ModelBase):
    name: str
    manufacturer: str
    length: float
    width: float


class ModelUpdate(ModelBase):
    name: Optional[str] = None
    manufacturer: Optional[str] = None
    length: Optional[float] = None
    width: Optional[float] = None


class Model(ModelBase):
    id: int
    name: str
    manufacturer: str
    length: float
    width: float
