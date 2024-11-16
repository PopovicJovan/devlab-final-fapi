from typing import Optional

from fastapi import HTTPException


class BaseException(HTTPException):
    def __init__(self,
                 detail: str, status_code: int = 422,
                 additional_info: Optional[str] = None
                 ):
        self.status_code = status_code
        self.detail = detail
        self.additional_info = additional_info
        super().__init__(status_code=status_code, detail=detail)


class UserNotFound(BaseException):
    def __init__(self,
                 detail: str, status_code: int = 404,
                 additional_info: Optional[str] = None
                 ):
        self.status_code = status_code
        self.detail = detail
        self.additional_info = additional_info
        super().__init__(status_code=status_code, detail=detail)


class ValidationError(BaseException):
    def __init__(self,
                 detail: str, status_code: int = 422,
                 additional_info: Optional[str] = None
                 ):
        self.status_code = status_code
        self.detail = detail
        self.additional_info = additional_info
        super().__init__(status_code=status_code, detail=detail)
