from typing import Union

from fastapi import FastAPI
from app.routers.auth import router as r1

app = FastAPI()

app.include_router(r1)

