from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import *
from app.api import *
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield
    close_engine()
def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(api_router)
    return app

app = create_app()