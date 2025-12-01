import pytest
from sqlmodel import SQLModel,create_engine,Session


@pytest.fixture(name="engine")
def init_fixture():
    url = "sqlite:///testing.db"
    _engine = create_engine(url,echo=True,connect_args={"check_same_thread": False})

    with _engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON")
        #查询
        result = conn.exec_driver_sql("PRAGMA foreign_keys")
        if result and result.fetchone() == (1,):
            print("sqlite 外键已开启")
        else:
            print("sqlite 外键未开启")
    return _engine

@pytest.fixture(name="init_db")
def init_db_and_tables(engine):
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session

def exec_sql(stmt,session):
    results = session.exec(stmt).all()
    for menu in results:
        print(menu.id,menu.name,menu.path)

