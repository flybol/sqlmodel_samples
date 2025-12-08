from ..models.user_model import UserBasePublic, UserFlagsInternal, Field


class UserCreate(UserBasePublic):
    """创建用户请求"""

    password: str = Field(min_length=8, max_length=32)


class UserUpdate(UserBasePublic):
    """更新用户请求"""

    password: str | None = Field(min_length=8, max_length=32)


class UserReadSelf(UserBasePublic):
    """用户信息返回"""

    id: int
    is_active: bool


class UserReadAdmin(UserBasePublic, UserFlagsInternal):
    """管理员用户信息返回"""

    id: int
