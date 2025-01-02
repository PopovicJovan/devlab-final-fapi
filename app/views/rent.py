from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, and_ , or_
from app.models.rent import Rent
from app.models.user import User
from app.schemas.rent import RentCreate
from app.views.yacht import YachtView
import app.exceptions as exc


class RentView:
    @classmethod
    def create_rent(cls, db: Session, rent_data: RentCreate, current_user:User)->Rent:
        try: yacht = YachtView.get_yacht_by_id(db, rent_data.yacht_id)
        except exc.ModelNotFound as e: raise e

        if not YachtView.yacht_is_available_now_for_rent(db, yacht):
            raise exc.NotAvailable("Yacht is not available for rent at the moment")

        overlapping_rent = db.execute(
            select(Rent).where(
                Rent.yacht_id == rent_data.yacht_id,
                or_(
                    and_(Rent.start_date <= rent_data.end_date, Rent.end_date >= rent_data.start_date),
                    and_(Rent.start_date <= rent_data.start_date, Rent.end_date >= rent_data.end_date)
                )
            )
        ).first()

        if overlapping_rent:
            raise exc.NotAvailable("The yacht is already rented for the selected dates!")

        start_date = rent_data.start_date
        end_date = rent_data.end_date
        days = (end_date - start_date).days

        total_price = days * yacht.rent_price
        user_id=current_user.id
        new_rent = Rent(
            yacht_id=rent_data.yacht_id, start_date=rent_data.start_date,
            end_date=rent_data.end_date,user_id=user_id,
            total_price=total_price
        )
        db.add(new_rent)
        return new_rent
    

    @classmethod
    def cancel_rent(cls, db: Session, rent_id: int, current_user: User) -> str:
        try:
            rent = db.execute(select(Rent).where(Rent.id == rent_id)).scalar_one_or_none()
            if not rent:
                raise ValueError(f"Rent with ID {rent_id} not found.")
            if rent.user_id != current_user.id and not current_user.admin:
                raise PermissionError("You do not have permission to cancel this rent")

            db.delete(rent)
            db.commit()
        except ValueError as ve:
            raise ve 
        except Exception as e:
            print(f"Error in cancel_rent: {e}")
            raise RuntimeError("An unexpected error occurred while canceling the rent")


    @classmethod
    def get_active_rents(cls, db: Session, yacht_id: int):
        return db.execute(select(Rent).where(
            Rent.yacht_id == yacht_id,
            Rent.end_date >= datetime.now().date()
        )).scalars().all()
