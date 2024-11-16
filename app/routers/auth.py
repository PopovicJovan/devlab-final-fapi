from fastapi import APIRouter

from app.exceptions import ValidationError
from app.schemas import auth, user
from app.database.database import db
from app.views.auth import AuthView
import bcrypt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=user.User)
def register(db: db, userdata: auth.Register):
    try:
        password = userdata.password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = AuthView.register(db=db, userdata=userdata)
        user.password = hashed_password
        db.commit()
        db.refresh(user)
        return user
    except ValidationError as e:
        raise e
