from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.exceptions import ValidationError
from app.schemas import auth, user
from app.database.database import db
from app.schemas.auth import Login
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

@router.post("/login", response_model=auth.Token)
def login(db: db, userdata: OAuth2PasswordRequestForm = Depends()) -> auth.Token:
    try:
        userdata = Login(username=userdata.username, password=userdata.password)
        token, user = AuthView.login(db=db, userdata=userdata)
        return auth.Token(access_token=token, token_type="bearer")
    except ValidationError as e:
        raise e
