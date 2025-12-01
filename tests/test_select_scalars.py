from sqlmodel import Session,select,col
from models.models_v2 import *  
def test_scalar(session:Session):
    stmt = select(Menu.id)
    result = session.exec(stmt)
    print(result.all())

    stmt = select(Menu.name).where(Menu.id==1)
    result = session.exec(stmt).one_or_none()
    print(result)
    

def test_batch_handler(session:Session):
    stmt = select(Menu)
    result = session.exec(stmt)
    batch = result.fetchmany(10)
    while batch:
        for row in  batch:
            print(row.name)
        print("-"*20)
        batch = result.fetchmany(10)

def test_partition_handler(session:Session):
    stmt = select(Menu).execution_options(yield_per=5)
    result = session.exec(stmt)
    for batch in result.partitions(5):
        for menu in batch:
            print(menu.name)
        print("-"*20)

# “禁止删除有子节点的菜单”。
def test_delete_menu_safe(session:Session):
    menu_id: int = 2
    menu = session.get(Menu, menu_id)
    if not menu:
        print("菜单不存在")
        return

    # 查询是否有子菜单
    stmt = select(Menu).where(col(Menu.parent_id) == menu_id)
    has_children = session.exec(stmt).first()
    if has_children:
        print("不能直接删除：存在子菜单")
        return

    session.delete(menu)
    session.commit()


# 一次性拿到父/子关系，构建树结构

def test_list_child_menus(session:Session):
    """ 
    利用 Relationship 直接访问 menu.children

    """
    #1. 先拿到所有顶级菜单
    stmt = select(Menu).where(col(Menu.parent_id).is_(None))
    roots = session.exec(stmt).all()

    for root in roots:
        print(f"[{root.id}] {root.name}")
        #children 是关系字段（懒加载）
        for child in root.children:
            print(f"  - [{child.id}] {child.name}")

# 从一条菜单向上找完整路径（面包屑）
# 例如：
# “系统管理 / 用户管理 / 新增用户”
def test_query_menu_path(session:Session):
    menu_id: int = 2
    menu = session.get(Menu, menu_id)
    if not menu:
        print("菜单不存在")
        return []

    path = []
    # 获取父级菜单
    parent = menu.parent
    path = [menu.name]
    while parent:
        path.append(parent.name)
        parent = parent.parent
