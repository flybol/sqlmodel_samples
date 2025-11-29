
from sqlmodel import Field,SQLModel
from rbac0.base_model import *

class UserBase(RBACBase,TimestampMixin):
    
    username: str = Field(index=True,max_length=32)
    full_name: str | None = Field(default=None,max_length=64)
    email: str | None = Field(default=None,max_length=64)
    is_enabled: bool = Field(default=True,description="是否已启用")

class User(IDMixin,UserBase,table=True):
    """ 用户表 """
    __tablename__:str = "users"
    hashed_password: str = Field(max_length=128)
    # 关系属性
    

class UserCreate(UserBase):
    """ 用户创建表 """
    password: str = Field(max_length=128)
    def to_create_dict(self):
        return self.model_dump(exclude_unset=True)

class UserUpdate(UserBase):
    """ 用户更新表 """
    password: str | None = Field(default=None,max_length=128)