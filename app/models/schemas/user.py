
from ..rbac_models import UserBase
from pydantic import Field

class UserCreate(UserBase):
    password:str = Field(min_length=6,max_length=32,examples=["123456"])