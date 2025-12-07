
import logging
from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

logger = logging.getLogger(__name__)
_engine: AsyncEngine|None = None

async def init_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            "sqlite+aiosqlite:///data.db",
            echo=True,
            connect_args={"check_same_thread": False},
            future=True,
            pool_pre_ping=True,
            pool_recycle=-1
        )
        async with _engine.connect() as conn:
            await conn.exec_driver_sql("PRAGMA foreign_keys=ON")
            result = await conn.exec_driver_sql("PRAGMA foreign_keys")
            if result and result.fetchone() == (1,):
                logger.info("sqlite 外键已开启")
            else:
                logger.info("sqlite 外键未开启")

SessionLocalFactory = async_sessionmaker(_engine,
                                         class_=AsyncSession,
                                         expire_on_commit=False)
async def get_session()->AsyncGenerator[AsyncSession,None]:
    async with SessionLocalFactory() as session:
        yield session

async def close_engine():
    assert _engine is not None, "Engine is not initialized"
    if _engine:
        await _engine.dispose()


from app.models.rbac_models import *
async def init_db_and_tables(is_drop:bool=False,is_create:bool=True):
    global _engine
    if _engine is None:
        await init_engine()

    assert _engine is not None, "Engine is not initialized"
    async with _engine.begin() as conn:
        if is_drop:
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.info("数据库表已删除")
        if is_create:
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("数据库表已创建")