from sqlmodel import Session,select,col
from models.models_v2 import *
from .conftest import *

@pytest.mark.skip
def test_init(init_db):pass

@pytest.mark.skip
def test_create_menu(session:Session):
    #创建顶级菜单
    sys_mgmt = Menu(name="系统管理",path="/system",sort_order=10)
    session.add(sys_mgmt)
    session.commit()
    session.refresh(sys_mgmt)  # 拿到自增 id
    # 2) 创建子菜单（指定 parent_id）
    user_mgmt = Menu(
        name="用户管理",
        path="/system/users",
        sort_order=10,
        parent_id=sys_mgmt.id,
    )
    role_mgmt = Menu(
        name="角色管理",
        path="/system/roles",
        sort_order=20,
        parent_id=sys_mgmt.id,
    )
    session.add_all([user_mgmt, role_mgmt])
    session.commit()

@pytest.mark.skip
def test_init_menus(session:Session):
    # 创建5个顶级菜单（根目录）
    sys_mgmt = Menu(name="系统管理", path="/system", sort_order=10)
    content_mgmt = Menu(name="内容管理", path="/content", sort_order=20)
    user_mgmt = Menu(name="用户中心", path="/user", sort_order=30)
    data_analysis = Menu(name="数据分析", path="/analysis", sort_order=40)
    settings = Menu(name="系统设置", path="/settings", sort_order=50)
    
    # 添加所有顶级菜单到session
    session.add_all([sys_mgmt, content_mgmt, user_mgmt, data_analysis, settings])
    session.commit()
    
    # 刷新获取所有顶级菜单的自增id
    session.refresh(sys_mgmt)
    session.refresh(content_mgmt)
    session.refresh(user_mgmt)
    session.refresh(data_analysis)
    session.refresh(settings)
    
    # 为每个根菜单创建3个子菜单
    # 1. 系统管理的子菜单
    sys_children = [
        Menu(name="用户管理", path="/system/users", sort_order=11, parent_id=sys_mgmt.id),
        Menu(name="角色管理", path="/system/roles", sort_order=12, parent_id=sys_mgmt.id),
        Menu(name="权限管理", path="/system/permissions", sort_order=13, parent_id=sys_mgmt.id)
    ]
    
    # 2. 内容管理的子菜单
    content_children = [
        Menu(name="文章管理", path="/content/articles", sort_order=21, parent_id=content_mgmt.id),
        Menu(name="分类管理", path="/content/categories", sort_order=22, parent_id=content_mgmt.id),
        Menu(name="标签管理", path="/content/tags", sort_order=23, parent_id=content_mgmt.id)
    ]
    
    # 3. 用户中心的子菜单
    user_children = [
        Menu(name="个人信息", path="/user/profile", sort_order=31, parent_id=user_mgmt.id),
        Menu(name="我的收藏", path="/user/favorites", sort_order=32, parent_id=user_mgmt.id),
        Menu(name="消息中心", path="/user/messages", sort_order=33, parent_id=user_mgmt.id)
    ]
    
    # 4. 数据分析的子菜单
    analysis_children = [
        Menu(name="访问统计", path="/analysis/visits", sort_order=41, parent_id=data_analysis.id),
        Menu(name="用户行为", path="/analysis/behavior", sort_order=42, parent_id=data_analysis.id),
        Menu(name="业务报表", path="/analysis/reports", sort_order=43, parent_id=data_analysis.id)
    ]
    
    # 5. 系统设置的子菜单
    settings_children = [
        Menu(name="基本设置", path="/settings/general", sort_order=51, parent_id=settings.id),
        Menu(name="安全设置", path="/settings/security", sort_order=52, parent_id=settings.id),
        Menu(name="通知设置", path="/settings/notifications", sort_order=53, parent_id=settings.id)
    ]
    
    # 添加所有子菜单
    all_children = (sys_children + content_children + user_children + 
                   analysis_children + settings_children)
    session.add_all(all_children)
    session.commit()
    
    print("菜单数据生成完成！")
    print(f"创建了5个根菜单和{len(all_children)}个子菜单")
def test_query_menu(session:Session):
    """
    简单查询（查所有菜单、查顶级、查某菜单的子菜单）
    """
    stmt = select(Menu).order_by(col(Menu.sort_order))
    results = session.exec(stmt).all()
    for menu in results:
        print(menu.id,menu.name,menu.path)

def test_list_root_menus(session:Session):
    """
    获取所有顶级菜单
    """
    stmt = (
        select(Menu)
        .where(
            # 查询filed是null
            col(Menu.parent_id).is_(None)
        )
        .order_by(col(Menu.sort_order))
    )
    exec_sql(stmt,session)

# 查某个菜单的直接子菜单：
def test_list_child_menus(session:Session):
    """
    获取某个菜单的直接子菜单
    """
    parent_id = 1
    stmt = (
        select(Menu)
        .where(
            # 获取某个菜单的直接子菜单
            col(Menu.parent_id) == parent_id
        )
        .order_by(col(Menu.sort_order))
    )
    exec_sql(stmt,session)


def test_rename_menum(session:Session):
    """重命名菜单"""
    menu_id = 2
    menu = session.get(Menu,menu_id)
    if menu is None:
        print("菜单不存在")
        return
    menu.name = "用户管理"
    session.add(menu)
    session.commit()

#修改父级（移动菜单到其他父节点）
def test_move_menu(session:Session):
    """
    new_parent_id = None 表示移动成顶级菜单
    """
    menu_id = 8
    new_parent_id = 2
    menu = session.get(Menu,menu_id)
    if menu is None:
        print("菜单不存在")
        return
    menu.parent_id = new_parent_id
    session.add(menu)
    session.commit()
def delete_menu_safe(menu_id: int,session: Session):
    """“禁止删除有子节点的菜单”。"""
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

from collections import defaultdict
# 例子：递归删除节点及所有子孙
def delete_menu_with_children(session:Session):
    menu_id = 1
    # 拿到所有菜单构建 children_map
    all_menus = session.exec(select(Menu)).all()
    children_map: dict[int, list[Menu]] = defaultdict(list)
    target_menu: Menu | None = None

    for m in all_menus:
        if m.parent_id is not None:
            children_map[m.parent_id].append(m)
        if m.id == menu_id:
            target_menu = m

    if not target_menu:
        print("菜单不存在")
        return
    
    to_delete_ids: list[int] = []
    def collect_descendants(m: Menu):
        if m.id is None:
            return
        to_delete_ids.append(m.id)
        for child in children_map.get(m.id, []):
            collect_descendants(child)

    collect_descendants(target_menu)
    # 批量删除
    for mid in to_delete_ids:
        obj = session.get(Menu, mid)
        if obj:
            session.delete(obj)

    session.commit()
    print("已删除节点及其所有子孙：", to_delete_ids)