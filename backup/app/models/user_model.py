from .base import Field, ORMBase, SoftDeleteMixin, AuditMixin, IDMixin


class UserBasePublic(ORMBase):
    """用户基础信息"""

    username: str = Field(
        min_length=4, max_length=64, index=True, unique=True, description="用户名唯一"
    )
    email: str | None = Field(
        min_length=4, max_length=64, index=True, unique=True, description="邮箱唯一"
    )
    phone: str | None = Field(
        min_length=11, max_length=11, index=True, unique=True, description="手机唯一"
    )


class UserFlagsInternal(ORMBase):
    """内部控制字段"""

    is_active: bool = Field(default=True, description="是否启用")
    is_superuser: bool = Field(default=False, description="是否是超级用户")


class User(
    AuditMixin, SoftDeleteMixin, UserFlagsInternal, UserBasePublic, IDMixin, table=True
):
    """用户表"""

    __tablename__: str = "sys_user"
    hashed_password: str = Field(min_length=8, max_length=128, description="加密密文")
