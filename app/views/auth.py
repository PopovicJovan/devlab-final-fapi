import os
from datetime import timedelta, datetime, timezone

from sqlalchemy.orm import Session

from app.schemas.auth import Register, Login
from app.schemas.user import User as UserSchema
from app.models.user import User
from app.views.user import UserView
from app.exceptions import ValidationError
import bcrypt, jwt
from dotenv import load_dotenv



class AuthView:
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = 'HS256'

    @classmethod
    def register(cls, db: Session, userdata: Register) -> User:
        user = UserView.get_user_by_email(db=db, email=userdata.email)
        if user is not None:
            raise ValidationError(detail='Email already in use')
        password = userdata.password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(**userdata.model_dump())
        user.password = hashed_password
        db.add(user)
        return user

    @classmethod
    def token_create(cls, db: Session, user_data: dict, expires_delta: timedelta | None = None):
        to_encode = user_data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def login(cls, db: Session, userdata: Login) -> (str, User):
        user = UserView.get_user_by_email(db=db, email=userdata.email)
        if user is None:
            raise ValidationError(detail='Invalid credentials', status_code=400)
        if not bcrypt.checkpw(userdata.password.encode('utf-8'), user.password.encode('utf-8')):
            raise ValidationError(detail='Invalid credentials', status_code=400)
        userdata = {
            "email": userdata.email
        }
        token = cls.token_create(db=db, user_data=userdata)
        return token, user
