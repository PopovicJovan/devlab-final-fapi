from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
import app.exceptions as exc
from app.database.database import db
from app.views.user import UserView
from app.schemas import user

router = APIRouter(prefix="/user", tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/show", response_model=user.User)
def get_user_by_token(db: db, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        user = UserView.get_user_by_token(db, token)
        return user
    except (exc.TokenExpired, exc.InvalidToken, exc.UserNotFound) as e:
        raise e
