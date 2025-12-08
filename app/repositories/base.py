from typing import Generic, TypeVar, Type
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from core.repository_registry import register_repository
from app.models.base import ORMBase

ModelType = TypeVar("ModelType", bound=ORMBase)


class BaseRepository(Generic[ModelType]):
    """
    约定：Repository 不负责 commit/rollback，只负责数据操作和 flush/refresh。
    """

    def __init__(
        self,
        session: AsyncSession,
        model: Type[ModelType],
    ):
        self.model = model
        self.session = session

    async def get(self, id: int) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.exec(stmt)
        return result.one_or_none()

    async def add(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj
