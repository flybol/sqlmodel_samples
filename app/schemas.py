from typing import Literal
from pydantic import BaseModel
from .models import *

class DepartmentPublic(DepartmentBase):
    id:int

class DepartmentPublicWithEmployees(DepartmentBase):
    id:int
    employees: List["EmployeePublic"] = []

class DepartmentCreate(DepartmentBase):
    ...

class UpdateDepartment(SQLModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    employee_ids: Optional[List[int]] = None

class CommonParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"

class EmployeePublic(EmployeeBase):
    id:int
    