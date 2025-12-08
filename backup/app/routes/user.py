from fastapi import APIRouter
from .deps import SessionDep
from ..schemas.user_schema import UserCreate, UserReadSelf
from ..services.user_service import get_user_service

router = APIRouter()


@router.post("/", response_model=UserReadSelf)
async def create_user(*, session: SessionDep, user_create: UserCreate):
    user_service = await get_user_service(session)
    return user_service.create_user(user_create)
