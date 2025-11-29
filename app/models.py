from typing import Optional,List
from sqlmodel import SQLModel,Field,Relationship
from enum import Enum

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class DepartmentBase(SQLModel):
    name:str = Field(index=True)
    description: str|None = Field(default="描述")

class Department(DepartmentBase,table=True):
    __tablename__:str = "department"
    id: Optional[int] = Field(default=None, primary_key=True)
    employees: Optional[List["Employee"]] = Relationship(back_populates="department")


class EmployeeBase(SQLModel):
    name:str = Field(index=True)
    gender: Gender = Field(default=Gender.OTHER)
    age: int = Field(default=0,ge=0,le=120)
    salary: float = Field(default=0.0,ge=0.0)
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")

class Employee(EmployeeBase,table=True):
    __tablename__:str = "employee"
    id: Optional[int] = Field(default=None, primary_key=True)
    department: Optional[Department] = Relationship(back_populates="employees")

