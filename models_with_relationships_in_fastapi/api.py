
from fastapi import APIRouter,HTTPException,Query
from models import *
from deps import *
team_router = APIRouter(prefix="/teams",tags=["teams"])
hero_router = APIRouter(prefix="/heroes",tags=["heroes"])

def hash_password(password: str) -> str:
    # Use something like passlib here
    return f"not really hashed {password} hehehe"

@team_router.post("/",response_model=TeamPublic)
def create_team(team: TeamCreate,session: SessionDep):
    """ 创建团队 """
    team_db = Team.model_validate(team)
    session.add(team_db)
    session.commit()
    session.refresh(team_db)
    return team_db

@team_router.get("/{team_id}",response_model=TeamPublicWithHeroes)
def read_team(team_id: int,session: SessionDep):
    """ 读取团队 """
    team = session.get(Team,team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@team_router.get("/teams/", response_model=list[TeamPublic])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams

@team_router.patch("/{team_id}", response_model=TeamPublic)
def update_team(*,
                team_id: int,
                team: TeamUpdate,
                session: Session = Depends(get_session),
                ):
    """ 更新团队"""
    # 查询
    team_db = session.get(Team, team_id)
    if not team_db:
        raise HTTPException(status_code=404, detail="Team not found")
    # 构造更新数据
    team_data = team.model_dump(exclude_unset=True)
    # 覆盖从数据库查询的内容
    team_db.sqlmodel_update(team_data)
    session.add(team_db)
    session.commit()
    session.refresh(team_db)
    return team_db

@team_router.delete("/{team_id}")
def delete_team(team_id: int,session: SessionDep):
    """ 删除团队"""
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}


@hero_router.post("/",response_model=HeroPublic)
def create_heros(session: SessionDep,hero: HeroCreate):
    """ 创建英雄"""
    hashed_password = hash_password(hero.password)
    extra_data = {"hashed_password": hashed_password}

    hero_db = Hero.model_validate(hero,update=extra_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@hero_router.get("/{hero_id}",response_model=HeroPublicWithTeam)
def read_hero(hero_id: int,session: SessionDep):
    """ 读取英雄 """
    hero = session.get(Hero,hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
@hero_router.get("/", response_model=list[HeroPublic])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@hero_router.patch("/{hero_id}", response_model=HeroPublic)
def update_hero(*,
                hero_id: int,
                hero: HeroUpdate,
                session: Session = Depends(get_session),
                ):
    """ 更新英雄 """
    # 获取
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    # 构造更新数据
    # hero_data = hero.model_dump(exclude_unset=True)
    # extra_data = {}
    # if "password" in hero_data:
    #     hashed_password = hash_password(hero_data["password"])
    #     extra_data.update({"hashed_password": hashed_password})
    hero_data = hero.to_update_model()
    # 数据校验
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db
    
