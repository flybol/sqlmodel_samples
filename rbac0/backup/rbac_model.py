
import enum
from re import I
from rbac0.user_model import User,SQLModel,Field
from rbac0.role_model import Role,IDMixin
from rbac0.permission_model import Permission
from datetime import datetime
from typing import List,Optional
from enum import Enum

class UserRoleLink(SQLModel):
    __tablename__:str = "user_role_link"
    user_id: int = Field(default=None, foreign_key="users.id",primary_key=True)
    role_id: int = Field(default=None, foreign_key="roles.id",primary_key=True)
    # ⭐ 关系级别的状态
    # is_enabled: bool = Field(default=True, description="该用户-角色关系是否启用")
    # granted_at: datetime = Field(default_factory=datetime.now, description="授予时间")
    # revoked_at: datetime | None = Field(default=None, description="撤销时间")
    # granted_by: int | None = Field(default=None, description="谁授予的")
    # expire_at: datetime | None = Field(default=None, description="角色过期时间")

class RolePermissionLink(SQLModel):
    __tablename__:str = "role_permission_link"
    role_id: int = Field(default=None, foreign_key="roles.id",primary_key=True)
    permission_id: int = Field(default=None, foreign_key="permissions.id",primary_key=True)

# ====== 辅助枚举：菜单类型 ======
@enum.unique
class MenuType(Enum):
    CATALOG = "catalog"  # 目录：只做分组，不可点击路由
    MENU = "menu"        # 菜单：有路由，有页面
    BUTTON = "button"    # 按钮：页面内部操作（新增、删除等）

# ====== 系统菜单模型 ======
class SystemMenuBase(IDMixin):
    # === 基本信息 ===
    name: str = Field(description="菜单名称，例如：用户管理")
    code: str = Field(
        description="菜单编码，前后端约定使用，如 system:user:manage",
        index=True,
    )
    type: MenuType = Field(
        default=MenuType.MENU,
        description="菜单类型：目录/菜单/按钮",
    )

    # === 路由相关 ===
    path: Optional[str] = Field(
        default=None,
        description="前端路由路径，如 /system/users",
    )
    component: Optional[str] = Field(
        default=None,
        description="前端组件路径，如 system/UserList",
    )
    icon: Optional[str] = Field(
        default=None,
        description="图标名称，由前端约定，例如 'UserOutlined'",
    )

    # === 树形结构 ===
    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="sys_menus.id",
        description="父菜单ID，根节点为 NULL",
    )
    sort_order: int = Field(
        default=0,
        description="排序号，数字越小越靠前",
    )

    # === 显示/状态控制 ===
    is_visible: bool = Field(
        default=True,
        description="是否在菜单中显示（有时需要隐藏路由）",
    )
    is_enabled: bool = Field(
        default=True,
        description="是否启用，禁用后不展示也不允许访问",
    )
class SystemMenu():
    """
    后台管理系统菜单表：
    - 支持多级菜单（自引用 parent_id）
    - 支持目录 / 菜单 / 按钮 三种类型
    - 可选绑定一个权限，用于基于权限过滤菜单
    """
    __tablename__:str = "sys_menus"

