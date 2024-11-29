from typing import Union

from fastapi import FastAPI
from app.routers.auth import router as r1
from app.routers.user import router as r2
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()
app = FastAPI()

origins = [
# Custom origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(r1)
app.include_router(r2)

