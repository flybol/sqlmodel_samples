from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from sqlalchemy import func, Column, DateTime


class IDMixin(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True, description="自增主键Id")


class AuditMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now()),
        description="创建时间",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, nullable=True),
        description="更新时间",
    )

    created_by: int = Field(nullable=False, description="创建人Id")
    updated_by: Optional[int] = Field(
        default=None, nullable=True, description="最后修改人用户ID"
    )


class SoftDeleteMixin(SQLModel, table=False):
    is_deleted: bool = Field(default=False, description="是否删除")
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, nullable=True),
        description="删除时间",
    )
    deleted_by: Optional[int] = Field(
        default=None, nullable=True, description="删除人Id"
    )


class ORMBase(AuditMixin, table=False):
    pass


# =============================================


class UserRoleLink(SQLModel, table=True):
    __tablename__: str = "sys_user_role_link"
    user_id: int | None = Field(
        default=None, foreign_key="sys_user.id", primary_key=True
    )
    role_id: int | None = Field(
        default=None, foreign_key="sys_role.id", primary_key=True
    )


class RolePermissionLink(SQLModel, table=True):
    __tablename__: str = "sys_role_permission_link"
    role_id: int | None = Field(
        default=None, foreign_key="sys_role.id", primary_key=True
    )
    permission_id: int | None = Field(
        default=None, foreign_key="sys_permission.id", primary_key=True
    )


# =============================================


class UserBase(ORMBase):
    username: str = Field(max_length=64, index=True, unique=True)
    email: str = Field(max_length=64, index=True, unique=True)
    phone: str = Field(max_length=64, index=True, unique=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(IDMixin, UserBase, table=True):
    __tablename__: str = "sys_user"
    hashed_password: str = Field(max_length=128)
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRoleLink)


class RoleBase(ORMBase):
    name: str = Field(max_length=64, index=True, unique=True)
    code: str = Field(max_length=64, index=True, unique=True)
    description: str | None = Field(default=None, max_length=255)


class Role(IDMixin, RoleBase, table=True):
    __tablename__: str = "sys_role"

    users: List[User] = Relationship(back_populates="roles", link_model=UserRoleLink)
    permissions: List["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermissionLink
    )


class PermissionBase(ORMBase):
    name: str = Field(max_length=64, index=True, unique=True)
    code: str = Field(max_length=64, index=True, unique=True)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)


class Permission(IDMixin, PermissionBase, table=True):
    __tablename__: str = "sys_permission"
    roles: List[Role] = Relationship(
        back_populates="permissions", link_model=RolePermissionLink
    )
    menus: List["Menu"] = Relationship(back_populates="permission")


class MenuBase(ORMBase):
    name: str = Field(max_length=64, index=True, unique=True)
    code: str = Field(max_length=64, index=True, unique=True)
    description: str | None = Field(default=None, max_length=255)
    is_visible: bool = Field(default=True)
    path: str | None = Field(default=None, max_length=255)
    icon: str | None = Field(default=None, max_length=64)
    permission_id: int | None = Field(default=None, foreign_key="sys_permission.id")
    parent_id: int | None = Field(default=None, foreign_key="sys_menu.id")


class Menu(IDMixin, MenuBase, table=True):
    __tablename__: str = "sys_menu"
    parent: Optional["Menu"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Menu.id"},
    )
    children: List["Menu"] = Relationship(back_populates="parent")
    permission: Permission | None = Relationship(back_populates="menus")
