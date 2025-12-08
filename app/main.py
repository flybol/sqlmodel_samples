from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.logging import setup_logging
from app.commons.constants import config
from app.core.db import init_db_and_tables, close_engine
from app.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init db
    await init_db_and_tables(is_drop=True)
    yield
    await close_engine()


def create_app():
    setup_logging()
    app = FastAPI(lifespan=lifespan, **config["fastapi"])
    app.include_router(api_router)
    return app


app = create_app()
