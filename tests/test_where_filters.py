from sqlmodel import select,or_,col,and_,desc
from .conftest import *
def test_where_in(session:Session):
    # 使用col函数处理字段为：id:int|None
    stmt = select(Employee).where(col(Employee.id).in_([1,2,3]))
    results = session.exec(stmt).all()
    print(results)

def test_where_not_in(session:Session):
    stmt = select(Employee).where(col(Employee.id).not_in([1,2,3]))
    results = session.exec(stmt).all()
    print(results)

def test_where_like(session:Session):
    stmt = select(Employee).where(col(Employee.name).like('员工%'))
    # stmt = select(Employee).where(col(Employee.email).like('%@qq.com'))
    stmt2 = select(Employee).where(col(Employee.name).not_like('%测试%'))
    # 语法糖
    stmt3 = select(Employee).where(col(Employee.name).contains('测试'))
    stmt4 = select(Employee).where(col(Employee.name).startswith('测试'))
    stmt5 = select(Employee).where(col(Employee.name).endswith('测试'))
    results = session.exec(stmt).all()
    print(results)


def test_like_pattern():
    # 匹配“100%” 这个字符串
    # 比如我们用 '\' 作为转义字符
    pattern = r"%100\%%"  # 匹配 “100%” 这个文本
    stmt6 = select(Employee).where(col(Employee.name).like(pattern,escape="\\"))
    print(stmt6)

def test_where_between(session:Session):
    # stmt = select(Employee).where(col(Employee.salary).between(1000,5000))
    stmt = select(Employee).where(col(Employee.salary)>=5000)
    results = session.exec(stmt).all()
    print(results)

def test_where_mutil(session:Session):
    stmt = (
        select(Employee)
        # WHERE employee.id IN (?, ?, ?) AND employee.salary >= ?
        .where(
            col(Employee.id).in_([1,2,3]),
            col(Employee.salary)>=5000
        )
    )
    results = session.exec(stmt).all()
    print(results)

def test_where_or(session:Session):
    stmt = (
        select(Employee)
        .where(
            or_(
                col(Employee.id).in_([1,2,3]),
                col(Employee.salary)>=5000
            )
        )
    )
    # print(stmt)
    stmt = (
        select(Employee)
        .where(
            col(Employee.id).not_in([1,2,3]),
        )
    )
    print(stmt)

def test_order_by_limit():
    stmt = (
        select(Employee)
        .where(
            col(Employee.id)>2,
            col(Employee.salary)>=5000
        ) #过滤条件
        .order_by(col(Employee.created_at).desc()) #排序
        .limit(10)  #限制
    )
    print(stmt)

    stmt =(
        select(Employee)
        .where(col(Employee.salary)>=5000)
        .order_by(col(Employee.created_at))
    )


def test_limit_offset():
    stmt = (
        select(Employee)
        .where(col(Employee.salary)>=5000)
        .order_by(col(Employee.created_at))
        .limit(10)
        .offset(0)
    )
    print(stmt)


def test_case1():
    """
    需求：
    查询“在职员工”，id > 10，并且 部门在 [1, 2, 3] 中，
    按 created_at 倒序，取第 2 页，每页 5 条。
    """
    stmt = (
        select(Employee)
        .where(
                and_(
                    col(Employee.id)>10,
                    col(Employee.status)== True,
                    col(Employee.department_id).in_([1,2,3])
                )
            )
            .order_by(col(Employee.created_at).desc())
            .limit(5)
            .offset(2)
    )

def test_case2():
    # 需求：名字里包含 "张"，按 created_at 倒序，只取 5 条
    stmt = (
        select(Employee)
        .where(
            col(Employee.name).contains("张")
        )
        .order_by(col(Employee.created_at).desc())
        .limit(5)
    )

def test_case3():
    # 需求：部门在 [1,2]，性别=男，状态=启用，按 id 升序，第 3 页，每页 10 条
    stmt = (
        select(Employee.department_id)
        .where(
            and_(
                col(Employee.department_id).in_([1,2]),
                Employee.gender == "男",
                Employee.status == True
            )
        )
        .order_by(col(Employee.id))
        .offset(3)
        .limit(10)
    )
    ## 需求：id > 100 且 (部门=1 或 部门=2)，按 id 倒序，前 20 个
    stmt = (
        select(Employee)
        .where(
            # and_(
            #     col(Employee.id)>100,
            #     or_(
            #         col(Employee.department_id) == 1,
            #         col(Employee.department_id) == 2,
            #     )
            # )
            col(Employee.id)>100,
            col(Employee.department_id).in_([1,2])
       )
       .order_by(desc(col(Employee.id)))
       .limit(20)
    )
    print(stmt)


def test_where_bettewn():
    stmt = (
        select(Employee)
        .where(
            col(Employee.salary).between(1000,5000)
        )
    )
    print(stmt)