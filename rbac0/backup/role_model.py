
from rbac0.base_model import *
class RoleBase(RBACBase,TimestampMixin):
    name: str = Field(index=True,description="角色名称（展示用）")
    code: str = Field(index=True,description="角色编码（例如: admin, finance_manager）")
    description: str|None = Field(default=None, description="角色描述")
    is_builtin: bool = Field(
        default=False,
        description="是否为系统内置角色（不可随便删除）",
    )

class Role(IDMixin,RoleBase,table=True):
    __tablename__:str = "roles"