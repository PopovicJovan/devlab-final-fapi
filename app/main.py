from typing import Union

from fastapi import FastAPI
from app.routers.auth import router as r1
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(r1)

