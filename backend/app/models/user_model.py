from sqlmodel import SQLModel, Field

from .base import BaseEntity


class UserBasePublic(SQLModel):
    username: str = Field(min_length=4, max_length=32, unique=True, index=True)
    email: str | None = Field(
        default=None, min_length=4, max_length=64, unique=True, index=True
    )
    phone: str | None = Field(
        default=None, min_length=11, max_length=11, unique=True, index=True
    )


class UserBaseInternal(SQLModel):
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBaseInternal, UserBasePublic, BaseEntity, table=True):
    __tablename__: str = "sys_user"
    hashed_password: str = Field(min_length=6, max_length=128)
