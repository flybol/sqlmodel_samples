from sqlalchemy.ext.asyncio import AsyncSession
from typing import Protocol, TypeVar, runtime_checkable

TUnitOfWork = TypeVar("TUnitOfWork", bound="AsyncUnitOfWorkProtocol")


@runtime_checkable
class AsyncUnitOfWorkProtocol(Protocol):
    """异步 UoW 接口定义，用于依赖倒置（service 只依赖这个协议）"""

    session: AsyncSession

    async def __aenter__(self: TUnitOfWork) -> TUnitOfWork: ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
