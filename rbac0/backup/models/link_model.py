from typing import Optional,List
from sqlmodel import SQLModel,Field,Relationship

from .role_model import Role
from .user_model import User

class UserRoleLink(SQLModel):
    """ 角色用户关联表 """
    __tablename__:str = "sys_user_role_link"
    role_id: int = Field(default=None, foreign_key="roles.id",primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id",primary_key=True)