

from sqlmodel import select,func,col
from .conftest import *
from .models.models_v1 import *

def test_func_count():
    stmt = (
        select(func.count(col(Employee.id)))
    )
    print(stmt)

def test_group_count():
    stmt = (
        select(
            Employee.department_id,
            func.count(col(Employee.id)).label("employee_count"),
            func.avg(Employee.salary).label("avg_salary"),
        )
        .group_by(col(Employee.department_id))
        .order_by(col(Employee.department_id))
    )
    print(stmt)

    stmt = (
        select(
            Employee.department_id,
            func.count(col(Employee.id)).label("employee_count"),
        )
        .group_by(col(Employee.department_id))
        # HAVING 条件
        .having(func.count(col(Employee.id)) >= 10)
    )
    print(stmt)

def test_distinct():
    stmt = select(Employee.department_id).distinct()
    print(stmt)
    stmt = (
    select(Employee, Department)
        .outerjoin(
            Department,
            col(Employee.department_id) == Department.id,
        )
    )
    print(stmt)

def test_join1():
    #  
    stmt = (
        select(Employee, Department, Project)
        .join(Department, col(Employee.department_id) == Department.id)
        .join(Project, col(Project.employee_id) == Employee.id)
    )
    print(stmt)