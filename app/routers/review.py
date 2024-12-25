from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.schemas.review import ReviewCreate, ReviewResponse
from app.views.review import ReviewView
from app.views.user import UserView
from app.database.database import database
import app.exceptions as exc

router = APIRouter(prefix="/reviews", tags=["Reviews"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/", response_model=ReviewResponse)
def create_review(review_data: ReviewCreate, db: database, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user = UserView.get_user_by_token(db, token)
        return ReviewView.create_review(db, review_data, current_user)
    except exc.ModelNotFound as e: raise e
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        print(f"Unhandled error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{review_id}", response_model=str)
def delete_review(review_id: int, db: database, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user=UserView.get_user_by_token(db, token)
        return ReviewView.delete_review(db, review_id, current_user)
    except (exc.TokenExpired, exc.InvalidToken, exc.ModelNotFound, PermissionError) as e:
        raise e