from typing import Union

from fastapi import UploadFile
import uuid
import shutil
import os
import base64
import app.exceptions as exc
from sqlalchemy.orm import Session
from app.views.Auth.jwt import JWTHelper
from app.models.user import User


class UserView:
    IMAGE_ROOT = "./app/public/images/users"

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
        if not os.path.exists(os.path.abspath(cls.IMAGE_ROOT)):
            os.makedirs(os.path.abspath(cls.IMAGE_ROOT))
        if user.picture:
            image_path = f"{cls.IMAGE_ROOT}/{user.picture}"
            if os.path.exists(image_path):
                os.remove(image_path)
        unique_filename = f"{uuid.uuid4()}.jpg"
        image_path = f"{str(cls.IMAGE_ROOT)}/{unique_filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(picture.file, f)

        user.picture = unique_filename

    @classmethod
    def get_user_photo(cls, user: User) -> Union[None, str]:
        if not user.picture:
            return None

        image_path = f"{cls.IMAGE_ROOT}/{user.picture}"
        with open(image_path, "rb") as image:
            image = image.read()

        return base64.b64encode(image).decode("utf-8")
