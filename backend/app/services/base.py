# file: app/services/base.py

from __future__ import annotations
from typing import Callable, Generic, TypeVar
from app.core.uow_protocol import AsyncUnitOfWork

TUoW = TypeVar("TUoW", bound=AsyncUnitOfWork)
# 如果你以后会有多种 UoW 实现，可以把 bound 换成一个 UoW Protocol，而不是具体类


class BaseService(Generic[TUoW]):
    """
    所有 Service 的基类，负责统一持有 uow_factory。
    """

    def __init__(self, uow_factory: Callable[[], TUoW]) -> None:
        # 受保护属性，子类可以用
        self._uow_factory = uow_factory
