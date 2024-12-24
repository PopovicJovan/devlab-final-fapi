from datetime import datetime, date
from sqlalchemy import Integer, DateTime, func, Date, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

class Rent(Base):
    __tablename__ = 'rents'

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    yacht_id: Mapped[int] = mapped_column(Integer, ForeignKey('yachts.id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id')) 

    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    total_price: Mapped[float] = mapped_column(Float)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    yacht: Mapped["Yacht"] = relationship("Yacht")
    user: Mapped["User"] = relationship("User")

    reviews:Mapped[list["Review"]] = relationship("Review", back_populates="rent", cascade="all, delete-orphan")
