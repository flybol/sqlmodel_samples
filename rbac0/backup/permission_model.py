from rbac0.base_model import *
class PermissionBase(RBACBase,TimestampMixin):
    """权限表"""
    code: str = Field(index=True, description="权限编码（唯一，如: order.read）")
    name: str = Field(description="权限名称（展示用）")
    resource: str = Field(description="资源标识（如: order, user, report）")
    action: str = Field(description="操作标识（如: read, create, update, delete）")
    description: str|None = Field(default=None, description="权限说明")


class Permission(IDMixin,PermissionBase,table=True):
    """权限表"""
    __tablename__:str = "permissions"
    # 一般推荐用“资源+操作”的组合来表示权限