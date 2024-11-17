from fastapi import HTTPException

from app.config import Settings
from datetime import datetime, timezone, timedelta
import jwt


class JWTHelper:
    SECRET_KEY = Settings().SECRET_KEY
    ALGORITHM = 'HS256'

    @classmethod
    def token_create(cls, user_data: dict, expires_delta: timedelta | None = None):
        to_encode = user_data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def verify_token(cls, token: str):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")