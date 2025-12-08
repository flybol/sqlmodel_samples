from app.models.user_model import UserBasePublic, Field


class UserReadSelf(UserBasePublic):
    id: int
    is_active: bool


class UserCreate(UserBasePublic):
    password: str = Field(min_length=8, max_length=32)
