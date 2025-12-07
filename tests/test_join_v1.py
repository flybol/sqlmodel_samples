from typing import Optional, List
from sqlmodel import Field, Session,func, SQLModel,Relationship,create_engine, select,col
import pytest
class Department(SQLModel, table=True):
    __tablename__:str = "department"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="部门名称")
    parent_id: Optional[int] = Field(default=None, foreign_key="department.id")
    parent: Optional["Department"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Department.id"},
    )
    children: List["Department"] = Relationship(back_populates="parent")

    company_id: Optional[int] = Field(default=None, foreign_key="company.id")
    employees: List["Employee"] = Relationship(back_populates="department")
    company: Optional["Company"] = Relationship(back_populates="departments")

class Employee(SQLModel, table=True):
    __tablename__:str = "employee"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="员工姓名")
    department_id: Optional[int] = Field(
        default=None, foreign_key="department.id", description="部门ID"
    )

    department: Optional[Department] = Relationship(back_populates="employees")

class Company(SQLModel, table=True):
    __tablename__:str = "company"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)

    departments: List[Department] = Relationship(back_populates="company")

sqlite_file_name = "testing.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True,connect_args={"check_same_thread": False})
@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session
def test_init_db_and_tables(session):
    with session.connection() as conn:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON")
        result = conn.exec_driver_sql("PRAGMA foreign_keys")
        if result.fetchone() == (1,):
            print("foreign_keys is ON")
        else:
            print("foreign_keys is OFF")
        SQLModel.metadata.create_all(engine)

def test_init_data(session):
    comps = [
        Company(name="公司A"),
        Company(name="公司B"),
        Company(name="公司C"),
    ]
    depts = [
        Department(name="部门A"),
        Department(name="部门B"),
        Department(name="部门C"),
        Department(name="部门D"),
    ]
    emps = [
        Employee(name="员工1"),
        Employee(name="员工2"),
        Employee(name="员工3"),
        Employee(name="员工4"),
        Employee(name="员工5"),
        Employee(name="员工6"),
        Employee(name="员工7"),
        Employee(name="员工8"),
        Employee(name="员工9"),
        Employee(name="员工10"),
    ]
    session.add_all(comps)
    session.add_all(depts)
    session.add_all(emps)
    session.commit()


def test_mutil_join(session:Session):
    stmt = (
        select(Employee, Department, Company)
        .join(Department,col(Employee.department_id )== Department.id)
        .join(Company,col(Department.company_id) == Company.id)
    )
    for emp,dept,comp in session.exec(stmt):
        print(emp.name,dept.name,comp.name)

def test_func(session:Session):
    """聚合统计——每个部门员工数量"""
    stmt =(
        select(Department.id,
               Department.name,
               func.count(col(Employee.id)).label("emp_count"))
        .join(Employee,col(Employee.department_id) == Department.id)
        .group_by(col(Department.id),Department.name)
    )
    for dept_id,dept_name,emp_count in session.exec(stmt):
        print(dept_id,dept_name,emp_count)

from sqlalchemy.orm import aliased
def test_self(session:Session):
    """自关联"""
    ParentDept = aliased(Department)
    stmt = (
        select(Department, ParentDept)
        .join(ParentDept,col(Department.parent_id) == ParentDept.id)
    )
    for dept,parent_dept in session.exec(stmt):
        print(dept.name,parent_dept.name)
    