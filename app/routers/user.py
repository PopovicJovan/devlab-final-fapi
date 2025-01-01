from typing import Annotated
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
import app.exceptions as exc
from app.database.database import database
from app.views.user import UserView
from app.schemas import user
from typing import List

router = APIRouter(prefix="/user", tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/show", response_model=user.UserWithSalesAndRents)
def get_user_by_token(db: database, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user = UserView.get_user_by_token(db, token)
        picture = UserView.get_user_photo(current_user)
        current_user.picture = f"data:image/jpeg;base64,{picture}" if picture else None
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


def is_admin(db: database, token: Annotated[str, Depends(oauth2_scheme)]) -> bool | None:
    try:
        current_user = UserView.get_user_by_token(db, token)
        return UserView.is_admin(current_user)
    except (exc.TokenExpired, exc.InvalidToken, exc.ForbidenException) as e:
        raise e

@router.get("/all-users", response_model=List[user.User], dependencies=[Depends(is_admin)])
def get_all_users(db: database):
    try:
        return UserView.get_all_users(db)
    except (exc.TokenExpired, exc.InvalidToken) as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{id}", response_model=user.UserWithSalesAndRents, dependencies=[Depends(is_admin)])
def get_user_by_id(db: database, id: int):
    try:
        user = UserView.get_user_by_id(db, id)
        picture = UserView.get_user_photo(user)
        user.picture = f"data:image/jpeg;base64,{picture}" if picture else None
        return user
    except (exc.UserNotFound) as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")