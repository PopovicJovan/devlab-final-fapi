from fastapi import Header
from app.config import Settings
from datetime import datetime, timezone, timedelta
import jwt
import app.exceptions as exc


class JWTHelper:
    SECRET_KEY = Settings().SECRET_KEY
    ALGORITHM = 'HS256'

    @classmethod
    def token_create(cls, user_data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = user_data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15000)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def verify_token(cls, token: str):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise exc.TokenExpired
        except jwt.InvalidTokenError:
            raise exc.InvalidToken

    @classmethod
    def verify_authorization(cls, Authorization: str = Header(...)) -> str:
        if not Authorization.startswith("Bearer "):
            raise exc.InvalidToken
        token = Authorization.split(" ")[1]

        try:
            cls.verify_token(token)
            return token
        except (exc.TokenExpired, exc.InvalidToken) as e:
            raise e
