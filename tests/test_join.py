from sqlmodel import Field, Session, SQLModel, create_engine, select,col
import pytest
class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")

sqlite_file_name = "testing.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True,connect_args={"check_same_thread": False})
@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session
def test_init_data(session: Session):
    with session.connection() as conn:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON")
        result = conn.exec_driver_sql("PRAGMA foreign_keys")
        if result.fetchone() == (1,):
            print("foreign_keys is ON")
        else:
            print("foreign_keys is OFF")
        SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        teams = [
            Team(name="TeamA", headquarters="上海"),
            Team(name="TeamB", headquarters="武汉"),
            Team(name="TeamC", headquarters="深圳"),
            Team(name="TeamD", headquarters="西安"),
            Team(name="TeamE", headquarters="广州"),
        ]
        heroes = [
            Hero(name="HeroA", secret_name="SecretA", team_id=1),
            Hero(name="HeroB", secret_name="SecretB", team_id=1),
            Hero(name="HeroC", secret_name="SecretC", team_id=2),
            Hero(name="HeroD", secret_name="SecretD", team_id=2),
        ]
        session.add_all(teams)
        session.add_all(heroes)
        session.commit()

def test_query_hero(session:Session):
    stmt = (
        select(Hero,Team)
        .join(Team)
        .where(Team.name == "TeamA")
    )
    result = session.exec(stmt)
    for hero,team in result:
        print(f"{hero.name} belongs to {team.name}")

def test_join_on(session:Session):
    stmt = (
        select(Hero,Team)
        .join(Team,col(Hero.team_id) == Team.id)
        .where(Team.name == "TeamA")
    )
    print(stmt)

def test_left_join(session:Session):
    """ 找到没有加入团队的英雄"""
    stmt = (
        select(Hero,Team)
        # 左外连接
        .outerjoin(Team,col(Hero.team_id)==Team.id)
        .where(col(Team.id).is_(None))
    )
    # print(stmt)
    for hero,team in session.exec(stmt):
        print(f"{hero.name} belongs to {team.name}")