# file: app/api/deps.py
from typing import AsyncGenerator
from app.core.uow_protocol import AsyncUnitOfWork
from app.core.uow import get_uow_factory
from app.services.user_service import UserService


async def get_uow() -> AsyncGenerator[AsyncUnitOfWork, None]:
    uow_factory = get_uow_factory()
    async with uow_factory() as uow:
        yield uow


def get_user_service() -> UserService:
    uow_factory = get_uow_factory()
    return UserService(uow_factory=uow_factory)
