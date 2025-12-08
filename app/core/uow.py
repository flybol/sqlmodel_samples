from typing import Callable
from app.core.db import AsyncSessionFactory
from .uow_impl import SqlModelAsyncUnitOfWork

UnitOfWorkFactory = Callable[[], SqlModelAsyncUnitOfWork]


# 直接把这个函数当作“工厂函数”用
def get_uow_factory() -> SqlModelAsyncUnitOfWork:
    """创建一个新的 UoW 实例（一个请求/一个事务）"""
    return SqlModelAsyncUnitOfWork(AsyncSessionFactory)
