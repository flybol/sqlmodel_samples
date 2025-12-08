from typing import Optional, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from .protocols import AsyncUnitOfWorkProtocol

SessionFactory = Callable[[], AsyncSession]


class SqlModelAsyncUnitOfWork(AsyncUnitOfWorkProtocol):
    """基于 SQLModel / AsyncSession 的 UoW 实现"""

    def __init__(self, session_factory: SessionFactory):
        self._session_factory = session_factory
        self.session: Optional[AsyncSession] = None

    async def __aenter__(self) -> "SqlModelAsyncUnitOfWork":
        self.session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # 没有 session 直接返回（理论上不该发生，只是保护）
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
