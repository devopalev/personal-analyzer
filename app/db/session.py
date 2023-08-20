from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_async_session() -> SessionLocal:
    return SessionLocal()

