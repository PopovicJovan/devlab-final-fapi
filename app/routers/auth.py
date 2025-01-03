from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.background import BackgroundTasks

from app.exceptions import ValidationError
from app.schemas import auth, user
from app.database.database import database
from app.schemas.auth import Login
from app.views.Auth.auth import AuthView
from app.views.mail import MailView
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=user.User)
async def register(db: database, userdata: auth.Register, request: Request, bt: BackgroundTasks):
    try:
        current_user = AuthView.register(db=db, userdata=userdata)
        db.commit()
        db.refresh(current_user)
        bt.add_task(MailView.register_email, current_user, request)
        return current_user
    except ValidationError as e:
        raise e


@router.post("/login", response_model=auth.Token)
def login(db: database, userdata: OAuth2PasswordRequestForm = Depends()) -> auth.Token:
    try:
        userdata = Login(username=userdata.username, password=userdata.password)
        token, current_user = AuthView.login(db=db, userdata=userdata)
        return auth.Token(access_token=token, token_type="bearer")
    except ValidationError as e:
        raise e
