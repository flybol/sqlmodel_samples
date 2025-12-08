from datetime import datetime
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional,List


class ORMBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at:datetime = Field(default_factory=datetime.now)
    updated_at:Optional[datetime] = Field(default=None)


from enum import Enum
class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class UserRoleLink(SQLModel,table=True):
    __tablename__:str = "sys_user_role_link"
    user_id: int = Field(default=None,primary_key=True, foreign_key="sys_user.id")
    role_id: int = Field(default=None,primary_key=True, foreign_key="sys_role.id")

    # user: "User" = Relationship(back_populates="roles")
    # role: "Role" = Relationship(back_populates="users")

class RolePermissionLink(SQLModel,table=True):
    __tablename__:str = "sys_role_permission_link"
    role_id: int = Field(default=None,primary_key=True,foreign_key="sys_role.id")
    permission_id: int = Field(default=None,primary_key=True,foreign_key="sys_permission.id")



class User(ORMBase,table=True):
    __tablename__:str = "sys_user"
    username: str = Field(index=True,max_length=50)
    email: str = Field(index=True,max_length=64)
    gender: Gender = Field(default=Gender.MALE,max_length=10)
    is_active: bool = Field(default=True)

    roles: List["Role"] = Relationship(back_populates="users",link_model=UserRoleLink)
    addresses: List["Address"] = Relationship(back_populates="user",link_model=UserRoleLink)

class Address(ORMBase,table=True):
    __tablename__:str = "sys_address"
    user_id: int = Field(default=None, foreign_key="sys_user.id")
    street: str = Field(max_length=255)
    city: str = Field(max_length=255)
    state: str = Field(max_length=255)
    country: str = Field(max_length=255)
    zip_code: str|None = Field(default=None,max_length=255)

    user: User = Relationship(back_populates="addresses")

class Role(ORMBase,table=True):
    __tablename__:str = "sys_role"
    name: str = Field(index=True,max_length=50)
    description: str = Field(default=None,max_length=255)
    is_active: bool = Field(default=True)

    users: List[User] = Relationship(back_populates="roles",link_model=UserRoleLink)
    permissions: List["Permission"] = Relationship(back_populates="roles",link_model=RolePermissionLink)

class Permission(ORMBase,table=True):
    __tablename__:str = "sys_permission"
    name: str = Field(index=True,max_length=50)
    description: str|None = Field(default=None,max_length=255)
    code: str = Field(max_length=255)

    roles: List[Role] = Relationship(back_populates="permissions",link_model=RolePermissionLink)
    menus: List["SysMenu"] = Relationship(back_populates="permission")

class SysMenu(ORMBase,table=True):
    __tablename__:str = "sys_menu"
    name: str = Field(index=True,max_length=50)
    icon: str|None = Field(max_length=50)
    path: str = Field(max_length=255)
    is_menu: bool = Field(default=False)
    description: str|None = Field(max_length=255)
    parent_id: int|None = Field(default=None, foreign_key="sys_menu.id")
    is_active: bool = Field(default=True)
    perm_id: int|None = Field(default=None, foreign_key="sys_permission.id")
    permission: Permission|None = Relationship(back_populates="menus")
    children: List["SysMenu"] = Relationship(back_populates="parent")
    parent: "SysMenu | None" = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "SysMenu.id"},
    )
