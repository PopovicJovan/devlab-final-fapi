from typing import Annotated
from fastapi import APIRouter, UploadFile
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
import app.exceptions as exc
from app.database.database import database
from app.views.user import UserView
from app.schemas import user

router = APIRouter(prefix="/user", tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/show", response_model=user.User)
def get_user_by_token(db: database, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user = UserView.get_user_by_token(db, token)
        return current_user
    except (exc.TokenExpired, exc.InvalidToken, exc.UserNotFound) as e:
        raise e


@router.post("/upload-picture")
def upload_user_picture(db: database, picture: UploadFile, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user = UserView.get_user_by_token(db, token)
        UserView.user_upload_photo(current_user, picture)
        db.commit()
    except (exc.TokenExpired, exc.InvalidToken, exc.UserNotFound) as e:
        raise e
