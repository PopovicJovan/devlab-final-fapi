from sqlalchemy.orm import Session
from app.schemas.auth import Register, Login
from app.models.user import User
from app.views.user import UserView
from app.exceptions import ValidationError
import bcrypt
from app.views.Auth.jwt import JWTHelper


class AuthView:
    @classmethod
    def register(cls, db: Session, userdata: Register) -> User:
        user = UserView.get_user_by_email(db=db, email=userdata.email)
        if user:
            raise ValidationError(detail='Email already in use')
        user = UserView.get_user_by_username(db=db, username=userdata.username)
        if user:
            raise ValidationError(detail='Username already in use')

        password = userdata.password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(**userdata.model_dump())
        user.password = hashed_password

        db.add(user)
        return user

    @classmethod
    def login(cls, db: Session, userdata: Login) -> (str, User):
        user = UserView.get_user_by_username(db=db, username=userdata.username)
        if user is None:
            raise ValidationError(detail='Invalid credentials', status_code=400)
        if not bcrypt.checkpw(userdata.password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValidationError(detail='Invalid credentials', status_code=400)
        userdata = {
            "username": user.username,
            "email": user.email,
            "admin": user.admin
        }
        token = JWTHelper.token_create(user_data=userdata)
        return token, user
