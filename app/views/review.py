from sqlalchemy.orm import Session
from sqlalchemy import select, delete
import app.exceptions as exc
from app.models.review import Review
from app.models.rent import Rent
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse


class ReviewView:
    @classmethod
    def create_review(cls, db: Session, review_data: ReviewCreate, current_user:User) -> ReviewResponse:
        rent = db.execute(select(Rent).where(Rent.id == review_data.rent_id)).scalar_one_or_none()
        if not rent: raise exc.ModelNotFound("Rent not found")
        
        if rent.user_id != current_user.id:
            raise PermissionError("You are not authorised to review this rent!")

        review = Review(**review_data.model_dump())
        db.add(review)
        db.commit()
        db.refresh(review)
        
        return review
       
    @classmethod
    def delete_review(cls, db: Session, review_id: int, current_user:User) -> None:
        review = cls.get_review_by_id(db, review_id)
        if not review: raise exc.ModelNotFound(detail="Review not found")

        rent = db.execute(select(Rent).where(Rent.id == review.rent_id)).scalar_one_or_none()
        if rent.user_id != current_user.id and not current_user.admin:
            raise PermissionError("You are not authorised to delete this review!")

        db.execute(delete(Review).where(Review.id == review_id))
        db.commit()

    @classmethod
    def get_review_by_id(cls, db: Session, review_id: int):
        return db.execute(select(Review).where(Review.id == review_id)).scalar_one_or_none()