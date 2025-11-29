from enum import Enum
from sqlmodel import Field, Relationship
from .base import *
from .link_model import *

class DataScope(Enum):
    ALL = "ALL"                   # 全部数据
    DEPT = "DEPT"                 # 本部门
    DEPT_AND_CHILD = "DEPT_CHILD" # 本部门及子部门
    SELF = "SELF"                 # 仅本人数据
    CUSTOM_DEPTS = "CUSTOM"       # 自定义部门集合

class RoleBase(ORMBaseWithActive):
    """ 角色基础信息 """
    code: str = Field(index=True,description="角色编码（例如: admin, finance_manager）")
    description: str|None = Field(default=None, description="角色描述")
    data_scope: DataScope = Field(
        default=DataScope.ALL,
        description="数据权限范围",
    )

class Role(IDMixin,RoleBase,table=True):
    """ 角色信息 """
    users:Optional[List[User]] = Relationship(back_populates="roles",link_model=UserRoleLink)