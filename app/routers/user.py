from fastapi import APIRouter
from fastapi.params import Depends
import app.exceptions as exc
from app.database.database import db
from app.views.Auth.jwt import JWTHelper
from app.views.user import UserView
from app.schemas import user


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/show", response_model=user.User)
def get_user_by_token(db: db, Authorization: str = Depends(JWTHelper.verify_authorization)):
    try:
        user = UserView.get_user_by_token(db, Authorization)
        return user
    except (exc.TokenExpired, exc.InvalidToken, exc.UserNotFound) as e:
        raise e
