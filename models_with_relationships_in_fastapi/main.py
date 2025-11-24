

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

# @app.post("/heroes/", response_model=HeroPublic)
# def create_hero(hero: HeroCreate,session: SessionDep):
#     hashed_password = hash_password(hero.password)
#     extra_data = {"hashed_password": hashed_password}
#     db_hero = Hero.model_validate(hero, update=extra_data)
#     session.add(db_hero)
#     session.commit()
#     session.refresh(db_hero)
#     return db_hero

# @app.get("/heroes/", response_model=list[HeroPublic])
# def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
#     with Session(engine) as session:
#         heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#         return heroes
    
# @app.get("/heroes/{hero_id}", response_model=HeroPublic)
# def read_hero(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         return hero
    
# @app.patch("/heroes/{hero_id}", response_model=HeroPublic)
# def update_hero(hero_id: int, hero: HeroUpdate):
#     with Session(engine) as session:
#         db_hero = session.get(Hero, hero_id)
#         if not db_hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         hero_data = hero.model_dump(exclude_unset=True)
#         extra_data = {}
#         # 判断密码是否被修改
#         if "password" in hero_data:
#             password = hero_data["password"]
#             hashed_password = hash_password(password)
#             extra_data["hashed_password"] = hashed_password
#         db_hero.sqlmodel_update(hero_data, update=extra_data)
#         session.add(db_hero)
#         session.commit()
#         session.refresh(db_hero)
#         return db_hero

# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(Hero, hero_id)
#         if not hero:
#             raise HTTPException(status_code=404, detail="Hero not found")
#         session.delete(hero)
#         session.commit()
#         return {"ok": True}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)