

from contextlib import asynccontextmanager
from api import *
from fastapi import FastAPI
from db import close_engine,create_db_and_tables

@asynccontextmanager 
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    close_engine()

app  = FastAPI(lifespan=lifespan)
app.include_router(team_router)
app.include_router(hero_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)