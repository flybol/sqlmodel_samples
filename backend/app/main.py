from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging import setup_logging
from app.api import root_api
from app.db.init_db import init_db_and_tables, close_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init db
    await init_db_and_tables(is_drop=True)
    yield
    await close_engine()


def create_app():
    setup_logging()
    app = FastAPI(lifespan=lifespan)
    app.include_router(root_api.api_router)
    return app


app = create_app()
