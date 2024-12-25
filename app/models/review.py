from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

class Review(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    rent_id: Mapped[int] = mapped_column(Integer, ForeignKey('rents.id'))
    comment: Mapped[str] = mapped_column(String(256))
    rate: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    rent: Mapped["Rent"] = relationship("Rent", back_populates="reviews")
    