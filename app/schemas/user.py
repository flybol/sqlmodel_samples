# from ..rbac_models import UserBase
# from app.core.security import get_hashed_password
# from pydantic import Field

# class UserCreate(UserBase):
#     #alias="password",将前端的password字段映射为hashed_password
#     hashed_password:str = Field(min_length=6,
#                          max_length=32,
#                          alias="password",
#                          examples=["123456"])

#     def update_hashed_password(self):
#         self.hashed_password = get_hashed_password(self.hashed_password)

# class UserRead(UserBase):
#     id:int
