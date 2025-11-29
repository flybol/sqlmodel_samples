from .base import *
from .link_model import *

class UserBase(ORMBaseWithActive):
    """ 用户基础信息 """
    username: str = Field(index=True,max_length=32)
    email: str | None = Field(default=None,max_length=64)


class User(IDMixin,UserBase,table=True):
    """ 用户表 """
    __tablename__:str = "sys_user"
    roles: Optional[List["Role"]] = Relationship(back_populates="users",link_model=UserRoleLink)
    
