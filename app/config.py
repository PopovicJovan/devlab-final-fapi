from typing import Union

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_USERNAME: Union[str, None]
    DB_PASSWORD: Union[str, None]
    DB_HOST: Union[str, None]
    DB_NAME: Union[str, None]
    DB_PORT: Union[str, None]
    SECRET_KEY: Union[str, None]

    MAIL_USERNAME: Union[str, None]
    MAIL_PASSWORD: Union[str, None]
    MAIL_FROM: Union[str, None]
    MAIL_PORT: Union[str, int]
    MAIL_SERVER: Union[str, None]
    MAIL_FROM_NAME: Union[str, None]


    @property
    def db_url(self) -> str:
        url = f"mysql+pymysql://{self.DB_USERNAME}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        if self.DB_PASSWORD:
            url = f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return url

    class Config:
        env_file = ".env"
        extra = "allow"
