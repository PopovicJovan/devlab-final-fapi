from fastapi import FastAPI
from app.routers import __all__ as all_routers
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from importlib import import_module
load_dotenv()
app = FastAPI()

origins = []  # custom origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module_name in all_routers:
    module = import_module(f"app.routers.{module_name}")
    app.include_router(module.router)
