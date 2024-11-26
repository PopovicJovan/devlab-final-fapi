import app.exceptions as exc
from sqlalchemy.orm import Session
from app.views.Auth.jwt import JWTHelper
from app.models.user import User

class UserView:

    @classmethod
    def get_user_by_email(cls, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @classmethod
    def get_user_by_username(cls, db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()

    @classmethod
    def get_user_by_token(cls, db: Session, token: str) -> User:
        try:
            user_data = JWTHelper.verify_token(token)
            user = cls.get_user_by_username(db, user_data.get("username"))
            if user is None:
                raise exc.UserNotFound
            return user
        except (exc.TokenExpired, exc.InvalidToken) as e:
            raise e


