from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base


class Status(Base):
    __tablename__ = 'statuses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(128), nullable=True)
