from typing import Union

from fastapi import FastAPI
from app.routers.auth import router as r1
from app.routers.user import router as r2
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(r1)
app.include_router(r2)

