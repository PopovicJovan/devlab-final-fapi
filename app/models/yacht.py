from datetime import datetime, date
from sqlalchemy import Integer, String, DateTime, func, Date, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base


class Yacht(Base):
    __tablename__ = 'yachts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model_id: Mapped[int] = mapped_column(Integer, ForeignKey('models.id'))
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'))

    name: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(Text)
    year: Mapped[date] = mapped_column(Date)

    sale_price: Mapped[float] = mapped_column(Float)
    rent_price: Mapped[float] = mapped_column(Float)

    picture: Mapped[str] = mapped_column(String(256), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    model: Mapped["Model"] = relationship("Model")
    status: Mapped["Status"] = relationship("Status")
