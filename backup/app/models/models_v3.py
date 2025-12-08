"""
自关联表设计
"""

from datetime import datetime
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,List


class ORMBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    # default_factory 表示每次都会调用函数，获取一个新的时间
    created_at:datetime = Field(default_factory=datetime.now)
    updated_at:Optional[datetime] = Field(default=None)

class Menu(ORMBase,table=True):
    __tablename__:str = "sys_menu"
    name: str = Field(index=True,max_length=50)
    parent_id: int|None = Field(default=None, foreign_key="sys_menu.id")
    name: str = Field(max_length=100, description="菜单名称")
    path: Optional[str] = Field(default=None, max_length=255, description="前端路由路径")
    sort_order: int = Field(default=0, description="同级菜单排序")
    is_enabled: bool = Field(default=True, description="是否启用")

    # 自关联关系
    parent: Optional["Menu"]= Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Menu.id"},
    )
    children: List["Menu"] = Relationship(back_populates="parent")
    permission_id: int|None = Field(default=None, foreign_key="sys_permission.id")
    permissions: List["Permission"] = Relationship(back_populates="menus")
    
class Permission(ORMBase,table=True):
    __tablename__:str = "sys_permission"
    name: str = Field(max_length=100, description="权限名称")
    code: str = Field(max_length=255, description="权限标识")
    description: str|None = Field(default=None,max_length=255, description="权限描述")
    is_enabled: bool = Field(default=True, description="是否启用")

    menus: List[Menu] = Relationship(back_populates="permissions")