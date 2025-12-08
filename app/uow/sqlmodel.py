from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Type, TypeVar, Generic, Dict, Any
from app.uow.base import AbstractUnitOfWork
from app.core.repository_registry import get_repository_class

SessionFactory = Callable[[], AsyncSession]
R = TypeVar("R")  # Repository 类型变量


class SqlModelUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: SessionFactory):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._repo_cache: Dict[Type[Any], Any] = {}

    async def __aenter__(self) -> "SqlModelUnitOfWork":
        self.session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session is None:
            return

        try:
            if exc_type:
                # 有异常 → 回滚
                await self.rollback()
            else:
                # 正常结束 → 提交事务
                await self.commit()
        finally:
            # 无论如何都要关闭连接
            await self.session.close()

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError(
                "Session is not initialized. Use 'async with uow:' block."
            )
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            return
        await self.session.rollback()

    def repo(self, name: str):
        repo_cls = get_repository_class(name)
        if name not in self._repo_cache:
            self._repo_cache[name] = repo_cls(self.session)
        return self._repo_cache[name]
