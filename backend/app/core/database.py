from typing import AsyncGenerator

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

Base = declarative_base()

# 创建数据库连接
async_engine = create_async_engine(
    settings.database_url,
    echo=False,
    echo_pool=False,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=5,
    connect_args={}
)

# 创建数据库会话
session_factory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=True,
    class_=AsyncSession
)


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        # 创建一个新的事务，半自动 commit
        async with session.begin():
            yield session
