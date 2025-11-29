
from fastapi import APIRouter,Query,HTTPException
from sqlmodel import select,func,in_
from .deps import *
from .schemas import *

emp_router = APIRouter()
dept_router = APIRouter()

@dept_router.post("/",response_model=Department)
def create_dept(*,session:SessionDep,
                dept:DepartmentCreate):
    # 构造数据
    dept_data = dept.model_dump(exclude_unset=True)
    # 数据校验
    dept_db = Department.model_validate(dept_data)
    # 插入数据库
    session.add(dept_db)
    session.commit()
    session.refresh(dept_db)
    return dept_db

@dept_router.get("/",response_model=list[DepartmentPublic])
def get_depts(*,session:SessionDep,
               common_params:CommonParams=Query()):
    stmt = select(Department).offset(common_params.offset).limit(common_params.limit)
    result = session.exec(stmt)
    return result.all()

@dept_router.put("/{dept_id}",response_model=DepartmentPublicWithEmployees)
def update_dept(*,session:SessionDep,
    dept_id:int,
    dept:UpdateDepartment):
    """ 更新部门信息 """
    db_dept = session.get(Department,dept_id)
    if not db_dept:
        raise HTTPException(status_code=404,detail="部门不存在")
    # 普通字段更新
    update_data = dept.model_dump(exclude_unset=True)
    employee_ids = update_data.pop("employee_ids",None)
    # 安全更新
    db_dept.sqlmodel_update(update_data)

    #更新部门员工信息
    if employee_ids is not None:
        if employee_ids:
            stmt = select(Employee).where(func.in_(employee_ids))
            employees = session.exec(stmt).all()
        else:
            employees = []

        db_dept.employees = employees
    session.add(db_dept)
    session.commit()
    session.refresh(db_dept)
    return db_dept














api_router = APIRouter()
api_router.include_router(emp_router,prefix="/employees",tags=["employees"])
api_router.include_router(dept_router,prefix="/departments",tags=["departments"])