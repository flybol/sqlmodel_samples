from .conftest import *
from .models.models_v1 import *
from sqlmodel import select,and_,or_,not_,col
def test_where_and_():
    stmt = select(Employee).where(and_(Employee.salary > 5000,
                                       Employee.gender == 'M',
                                       col(Employee.id).in_([1,2,3])))
    print(stmt)