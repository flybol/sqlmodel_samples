import random
from sqlmodel import create_engine,SQLModel,Session
import pytest
from random import randint
from .models.models_v1 import *
@pytest.fixture(name="session")
def session_fixture(request):
    """ Session fixture
    param[0]: is drop tables
    param[1]: is create tables
    """
    sqlite_db = "testing.db"
    url = f"sqlite:///{sqlite_db}"
    engine = create_engine(url,echo=True,connect_args={"check_same_thread": False})
    # SQLModel.metadata.drop_all(engine)
    # SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def get_random_age():
    return randint(18,120)

def get_random_gender():
    return random.choice(list(Gender))

def get_random_salary():
    salary = [3000,4000,5000,6000,7000,8000,9000,10000]
    return random.choice(salary)

@pytest.fixture(name="init_data")
def init_data(session:Session):
    depts = [
        Department(name="部门A"),
        Department(name="部门B"),
        Department(name="部门C"),
        Department(name="部门D"),
    ]
    emps = []
    for e in range(4):
        dept = depts.pop()
        emps.append(Employee(name=f"员工{e+1}",
                age=get_random_age(),
                gender=get_random_gender(),
                salary=get_random_salary(),
                department=dept))
    session.add_all(emps)
    session.commit()
    return len(emps)
