# file: app/core/uow_protocol.py

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable, TypeVar
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository  # 你前面定义的基类

TRepo = TypeVar("TRepo", bound=BaseRepository[Any])


@runtime_checkable
class AsyncUnitOfWork(AbstractAsyncContextManager["AsyncUnitOfWork"], Protocol):
    """
    UoW 协议接口（异步版）：
    - 是一个 async 上下文管理器
    - 内部持有一个 AsyncSession（可选暴露）
    - 能 commit / rollback
    - 能够按名称返回 Repository
    """

    session: AsyncSession  # 如果你希望在协议层也暴露 session，可以保留；不需要可以去掉

    async def __aenter__(self) -> "AsyncUnitOfWork": ...

    async def __aexit__(self, exc_type, exc, tb) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    def get_repo(self, name: str | type[TRepo]) -> BaseRepository[Any]:
        """
        提供一个通用的获取仓储的方法。
        至于 uow.user 这种动态属性访问，就作为实现类的“增强能力”，
        不必须写进协议（协议只描述最小依赖）。
        """
        ...
