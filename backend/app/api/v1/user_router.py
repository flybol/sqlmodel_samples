from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schema import UserCreate, UserReadSelf
from app.api.deps import get_user_service
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "/",
    response_model=UserReadSelf,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserReadSelf:
    """
    创建用户接口：
    - 入参：UserCreate
    - 出参：UserRead
    """
    user = await service.create_user(user_in)
    return UserReadSelf.model_validate(user)
