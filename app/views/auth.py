from sqlalchemy.orm import Session

from app.schemas.auth import Register
from app.models.user import User
from app.views.user import UserView
from app.exceptions import ValidationError


class AuthView:

    @staticmethod
    def register(db: Session, userdata: Register) -> User:
        user = UserView.get_user_by_email(db=db, email=userdata.email)
        if user is not None:
            raise ValidationError(detail='Email already in use')
        user = User(**userdata.model_dump())
        db.add(user)
        return user




