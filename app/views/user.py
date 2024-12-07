from fastapi import UploadFile
import uuid
import shutil
import os
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

    @classmethod
    def user_upload_photo(cls, user: User, picture: UploadFile) -> None:
        IMAGE_ROOT = "./app/public/images/users"
        if not os.path.exists(os.path.abspath(IMAGE_ROOT)):
            os.makedirs(os.path.abspath(IMAGE_ROOT))
        if user.picture:
            image_path = f"{IMAGE_ROOT}/{user.picture}"
            if os.path.exists(image_path):
                os.remove(image_path)
        unique_filename = f"{uuid.uuid4()}.jpg"
        image_path = f"{str(IMAGE_ROOT)}/{unique_filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(picture.file, f)

        user.picture = unique_filename
