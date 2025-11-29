"""
学习一对多的关系
"""
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,List

class ORMBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at:datetime = Field(default_factory=datetime.now)
    updated_at:datetime|None = Field(default=None)

class Gender(int,Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 0

class Employee(ORMBase,table=True):
    name:str = Field(index=True)
    age: int = Field(default=0,ge=0,le=120)
    gender: Gender = Field(default=1,ge=0,le=2)
    salary: float = Field(default=0.0,ge=0.0)
    status:bool = Field(default=True)
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    department: Optional["Department"] = Relationship(back_populates="employees")

class Department(ORMBase,table=True):
    name:str = Field(index=True)
    description: str|None = Field(default="描述")
    employees: Optional[List[Employee]] = Relationship(back_populates="department")
    status:bool = Field(default=True)

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    employee_id: int = Field(foreign_key="employee.id")