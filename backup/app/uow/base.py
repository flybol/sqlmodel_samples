from typing import Protocol, Callable
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractUnitOfWork(Protocol):
    session: AsyncSession

    async def __aenter__(self) -> "AbstractUnitOfWork": ...
    async def __aexit__(self, exc_type, exc, tb): ...

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


# 工厂类型：调用后返回一个 UoW 实例
UnitOfWorkFactory = Callable[[], AbstractUnitOfWork]
