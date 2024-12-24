from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = 'sales'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    yacht_id: Mapped[int] = mapped_column(Integer, ForeignKey('yachts.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="sales")
    yacht: Mapped["Yacht"] = relationship("Yacht")