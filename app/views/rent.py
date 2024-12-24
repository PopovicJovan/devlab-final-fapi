from sqlalchemy.orm import Session
from sqlalchemy import select, and_ , or_
from app.models.rent import Rent
from app.models.yacht import Yacht
from app.models.user import User
from app.schemas.rent import RentCreate, RentResponse

class RentView:
    @classmethod
    def create_rent(cls, db: Session, rent_data: RentCreate, current_user:User)->RentResponse:               
        yacht = db.execute(select(Yacht).where(Yacht.id == rent_data.yacht_id)).scalar_one_or_none()
        if not yacht:
            raise ValueError("Yacht not found") 
        
        overlapping_rent = db.execute(
            select(Rent).where(
                and_(
                    Rent.yacht_id == rent_data.yacht_id,
                    or_(
                        and_(Rent.start_date <= rent_data.start_date, Rent.end_date >= rent_data.start_date),
                        and_(Rent.start_date <= rent_data.end_date, Rent.end_date >= rent_data.end_date),
                        and_(Rent.start_date >= rent_data.start_date, Rent.end_date <= rent_data.end_date),
                        and_(Rent.end_date >= rent_data.start_date, Rent.end_date<=rent_data.end_date)
                    ),
                )
            )
        ).scalar_one_or_none()

        if overlapping_rent:
            raise ValueError("The yacht is already rented for the selected dates!")

        start_date = rent_data.start_date
        end_date = rent_data.end_date
        days = (end_date - start_date).days
        if days <= 0:
            raise ValueError("Invalid date range")

        total_price = days * yacht.rent_price
        user_id=current_user.id
        new_rent = Rent(**rent_data.model_dump(),user_id=user_id, total_price=total_price)
        db.add(new_rent)
        db.commit()
        db.refresh(new_rent)
        return RentResponse.model_validate(new_rent)
    

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
            return "Rent canceled successfully"
        except ValueError as ve:
            raise ve 
        except Exception as e:
            print(f"Error in cancel_rent: {e}")
            raise RuntimeError("An unexpected error occurred while canceling the rent")
