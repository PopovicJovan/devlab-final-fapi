from typing import Optional
from fastapi import HTTPException


class BaseException(HTTPException):
    def __init__(self,
                 detail: str = "Everything went ok.",
                 status_code: int = 200,
                 additional_info: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)
        self.additional_info = additional_info


class UserNotFound(BaseException):
    def __init__(self,
                 detail: str = "User Not Found",
                 status_code: int = 404,
                 additional_info: Optional[str] = None):
        super().__init__(detail=detail, status_code=status_code, additional_info=additional_info)


class ValidationError(BaseException):
    def __init__(self,
                 detail: str = "Validation Error",
                 status_code: int = 422,
                 additional_info: Optional[str] = None):
        super().__init__(detail=detail, status_code=status_code, additional_info=additional_info)


class TokenError(BaseException):
    def __init__(self,
                 detail: str,
                 status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)


class TokenExpired(TokenError):
    def __init__(self):
        super().__init__(detail="Token has expired")


class InvalidToken(TokenError):
    def __init__(self):
        super().__init__(detail="Invalid token")

class ModelInUse(BaseException):
    def __init__(self,
                 detail: str = "Model already exists",
                 status_code: int = 422,
                 additional_info: Optional[str] = None):
        super().__init__(detail=detail, status_code=status_code, additional_info=additional_info)

class ModelNotFound(BaseException):
    def __init__(self,
                 detail: str = "Model Not Found",
                 status_code: int = 404,
                 additional_info: Optional[str] = None):
        super().__init__(detail=detail, status_code=status_code, additional_info=additional_info)

class ForbidenException(BaseException):
    def __init__(self,
                 detail: str = "Forbidden",
                 status_code: int = 403,
                 additional_info: Optional[str] = None):
        super().__init__(detail=detail, status_code=status_code, additional_info=additional_info)