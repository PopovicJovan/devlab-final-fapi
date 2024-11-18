from typing import Union
from fastapi import APIRouter
from app.exceptions import ValidationError
from app.schemas import auth, user
from app.database.database import db
from app.views.Auth.auth import AuthView

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=user.User)
def register(db: db, userdata: auth.Register):
    try:
        user = AuthView.register(db=db, userdata=userdata)
        db.commit()
        db.refresh(user)
        return user
    except ValidationError as e:
        raise e


@router.post("/login", response_model=dict[str, Union[str, user.User]])
def login(db: db, userdata: auth.Login) -> dict[str, Union[str, user.User]]:
    try:
        token, user = AuthView.login(db=db, userdata=userdata)
        return {
            "user": user,
            "token": token
        }
    except ValidationError as e:
        raise e
