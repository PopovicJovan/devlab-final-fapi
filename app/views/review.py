from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from fastapi import HTTPException
from app.models.review import Review
from app.models.rent import Rent
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse


class ReviewView:
    @classmethod
    def create_review(cls, db: Session, review_data: ReviewCreate, current_user:User) -> ReviewResponse:
        rent = db.execute(select(Rent).where(Rent.id == review_data.rent_id)).scalar_one_or_none()
        if not rent:
            raise ValueError("Rent not found")
        
        if rent.user_id != current_user.id:
            raise PermissionError("You are not authorised to review this rent!")

        review = Review(**review_data.model_dump())
        if review.rate<1 or review.rate>5:
            raise PermissionError("Rate must be between 1 and 5!")
        db.add(review)
        db.commit()
        db.refresh(review)
        
        return review
       
    @classmethod
    def delete_review(cls, db: Session, review_id: int, current_user:User) -> str:
        review = db.execute(select(Review).where(Review.id == review_id)).scalar_one_or_none()
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")

        rent = db.execute(select(Rent).where(Rent.id == review.rent_id)).scalar_one_or_none()
        if rent.user_id != current_user.id and not current_user.admin:
            raise PermissionError("You are not authorised to delete this review!")

        db.execute(delete(Review).where(Review.id == review_id))
        db.commit()        
        return f"Review ID {review_id} deleted successfully"