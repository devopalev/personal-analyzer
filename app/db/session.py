from functools import wraps

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
    autoflush=False,
)


async def get_async_session() -> AsyncSession:
    return SessionLocal()


def session_wrapper(a_func):
    @wraps(a_func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get("session")

        if not session:
            kwargs["session"] = await get_async_session()

        result = await a_func(*args, **kwargs)

        if not session:
            await kwargs["session"].close()

        return result

    return wrapper
