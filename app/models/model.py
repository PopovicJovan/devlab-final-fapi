from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base


class Model(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    manufacturer: Mapped[str] = mapped_column(String(32), unique=True)
    length: Mapped[float] = mapped_column(Float)
    width: Mapped[float] = mapped_column(Float)
