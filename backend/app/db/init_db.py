import logging
from sqlmodel import SQLModel
from .session import engine

logger = logging.getLogger(__name__)


async def init_db_and_tables(is_drop: bool = False, is_create: bool = True) -> None:
    """初始化数据库表（示例）"""
    assert engine is not None, "Engine is not initialized"
    async with engine.begin() as conn:
        await conn.exec_driver_sql("PRAGMA foreign_keys=ON")
        result = await conn.exec_driver_sql("PRAGMA foreign_keys")
        if result and result.fetchone() == (1,):
            logger.info("sqlite 外键已开启")
        else:
            logger.info("sqlite 外键未开启")

        if is_drop:  # 删除表
            await conn.run_sync(SQLModel.metadata.drop_all)
            logger.info("已删除所有表")
        if is_create:  # 创建表
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("已创建所有表")


async def close_engine() -> None:
    """关闭数据库连接"""
    if engine is not None:
        await engine.dispose()
