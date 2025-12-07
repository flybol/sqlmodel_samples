
from fastapi import APIRouter
from app.models.schemas.user import *
from .deps import SessionDep
router = APIRouter()

@router.post("/")
async def create_user(*,session:SessionDep,
                      user:UserCreate):
    return user