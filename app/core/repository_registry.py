# core/repository_registry.py
from typing import Type, Dict, Any

# 仓储自动注册 / 装饰器 + Registry
_REPOSITORY_REGISTRY: Dict[str, Type[Any]] = {}


def register_repository(name: str):
    def decorator(cls: Type[Any]):
        _REPOSITORY_REGISTRY[name] = cls
        return cls

    return decorator


def get_repository_class(name: str) -> Type[Any]:
    return _REPOSITORY_REGISTRY[name]
