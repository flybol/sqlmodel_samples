# file: app/core/uow.py

from __future__ import annotations

from typing import Any, Dict, Callable

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.db.session import AsyncSessionFactory
from app.repositories.base import BaseRepository, _REPOSITORY_REGISTRY

from .uow_protocol import AsyncUnitOfWork, TRepo


class SqlModelAsyncUnitOfWork(AsyncUnitOfWork):
    """
    基于 SQLModel / AsyncSession 的 UoW 实现，遵守 AsyncUnitOfWork 协议。
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._repos: Dict[str, BaseRepository[Any]] = {}

    async def __aenter__(self) -> "SqlModelAsyncUnitOfWork":
        self.session = self._session_factory()

        for name, repo_cls in _REPOSITORY_REGISTRY.items():
            self._repos[name] = repo_cls(self.session)

        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self.session is not None, "Session not initialized"

        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()

    # ---------- 协议要求的方法 ---------- #

    async def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("Session not initialized")
        await self.session.commit()

    async def rollback(self) -> None:
        if self.session is None:
            raise RuntimeError("Session not initialized")
        await self.session.rollback()

    def get_repo(self, name: str | type[TRepo]) -> BaseRepository[Any]:
        try:
            key: str = ""
            if isinstance(name, type):
                key = name.__name__
            else:
                key = name
            return self._repos[key]
        except KeyError:
            raise AttributeError(
                f"Repository '{name}' not found. Registered: {list(self._repos.keys())}"
            )

    # ---------- 额外增强能力（非协议必须） ---------- #

    def __getattr__(self, item: str) -> Any:
        """
        支持 uow.user / uow.order 的动态属性访问。
        这不是协议要求的内容，是具体实现提供的方便能力。
        """
        if item in self._repos:
            return self._repos[item]
        raise AttributeError(
            f"'SqlModelAsyncUnitOfWork' object has no attribute '{item}'"
        )


# class SqlModelAsyncUnitOfWork:
#     """
#     使用 async_sessionmaker + 自动注册仓储 的 UoW 实现。

#     使用方式：
#     uow_factory = get_uow_factory()

#     async with uow_factory() as uow:
#         user = await uow.user.get_by_username("alice")
#         orders = await uow.order.list_by_user(user.id)
#     """

#     def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
#         self._session_factory = session_factory
#         self.session: AsyncSession | None = None
#         self._repos: Dict[str, BaseRepository[Any]] = {}

#     async def __aenter__(self) -> "SqlModelAsyncUnitOfWork":
#         self.session = self._session_factory()

#         # 基于 Registry 自动实例化所有仓储
#         for name, repo_cls in _REPOSITORY_REGISTRY.items():
#             self._repos[name] = repo_cls(self.session)

#         return self

#     async def __aexit__(self, exc_type, exc, tb) -> None:
#         assert self.session is not None, "Session not initialized"

#         try:
#             if exc_type:
#                 await self.session.rollback()
#             else:
#                 await self.session.commit()
#         finally:
#             await self.session.close()

#     # ------------- UoW 对外 API ------------- #

#     async def commit(self) -> None:
#         if self.session is None:
#             raise RuntimeError("Session not initialized")
#         await self.session.commit()

#     async def rollback(self) -> None:
#         if self.session is None:
#             raise RuntimeError("Session not initialized")
#         await self.session.rollback()

#     def get_repo(self, name: str) -> BaseRepository[Any]:
#         try:
#             return self._repos[name]
#         except KeyError:
#             raise AttributeError(
#                 f"Repository '{name}' not found. Registered: {list(self._repos.keys())}"
#             )

#     def __getattr__(self, item: str) -> Any:
#         """
#         支持 uow.user / uow.order 这种属性访问形式。

#         - 注册时用的 name 就是这里的属性名（@register_repository("user")）
#         """
#         if item in self._repos:
#             return self._repos[item]
#         # 避免无限递归
#         raise AttributeError(
#             f"'SqlModelAsyncUnitOfWork' object has no attribute '{item}'"
#         )


def get_uow_factory() -> Callable[[], SqlModelAsyncUnitOfWork]:
    """
    工厂函数：返回一个可调用对象，每次调用创建一个新的 UoW。
    可以在 FastAPI 依赖注入中使用。
    """
    return lambda: SqlModelAsyncUnitOfWork(AsyncSessionFactory)
