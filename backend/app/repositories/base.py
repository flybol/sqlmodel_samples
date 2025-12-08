# file: app/repositories/base.py

from __future__ import annotations

from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.base import BaseEntity

TModel = TypeVar("TModel", bound=BaseEntity)


class BaseRepository(Generic[TModel]):
    """所有仓储的抽象基类（非必须抽象基类，这里做一个通用 CRUD 实现）"""

    model: Type[TModel]  # 子类必须指定

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id_: Any) -> Optional[TModel]:
        stmt = select(self.model).where(self.model.id == id_)  # 约定模型有 id 字段
        result = await self.session.exec(stmt)
        return result.one_or_none()

    async def add(self, obj: TModel) -> TModel:
        self.session.add(obj)
        return obj

    async def delete(self, obj: TModel) -> None:
        await self.session.delete(obj)


# ------------------ Registry 部分 ------------------ #

_REPOSITORY_REGISTRY: Dict[str, Type[BaseRepository[Any]]] = {}


def register_repository(
    name: str | None = None,
) -> Callable[[Type[BaseRepository[Any]]], Type[BaseRepository[Any]]]:
    """
    装饰器：注册 Repository 到全局 Registry。

    使用方式：
    @register_repository("user")
    class UserRepository(BaseRepository[User]):
        ...
    """

    def decorator(cls: Type[BaseRepository[Any]]) -> Type[BaseRepository[Any]]:
        key = name or cls.__name__

        if key in _REPOSITORY_REGISTRY:
            raise ValueError(
                f"Repository name '{key}' already registered by {_REPOSITORY_REGISTRY[key]}"
            )

        _REPOSITORY_REGISTRY[key] = cls
        return cls

    return decorator


def get_repository_class(
    name: type[BaseRepository | str],
) -> Type[BaseRepository[Any]]:
    try:
        key: str = ""
        if isinstance(name, type):
            key = name.__name__
        else:
            key = name
        return _REPOSITORY_REGISTRY[key]
    except KeyError:
        raise KeyError(
            f"Repository '{key}' not found. Registered keys: {list(_REPOSITORY_REGISTRY.keys())}"
        )
