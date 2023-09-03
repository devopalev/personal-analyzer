import pytest_asyncio
from pytest_mock import MockerFixture
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.db.models.channels import TelegramChannel as ChannelModel
from app.db.models.users import User as UserModel


@pytest_asyncio.fixture()
async def db_session(mocker: MockerFixture):
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

    async_engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, future=True
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    mocker.patch(
        "app.db.session.get_async_session",
        return_value=TestingSessionLocal(),
    )

    with open("app/static/language_objects.sql", "r", encoding="utf-8") as file:
        dump_language = file.read()

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(dump_language))

        async with TestingSessionLocal(bind=conn) as session:
            yield session
            # await session.flush()
            # await session.rollback()
            await session.close()


@pytest_asyncio.fixture()
async def user_db(db_session: AsyncSession, user_test) -> AsyncSession:
    u = UserModel(
        id=1,
        telegram_id=user_test.id,
        fullname=user_test.id,
        username=user_test.username,
        language_code=user_test.language_code,
        active=True,
    )
    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)
    return u


@pytest_asyncio.fixture()
async def channel_db(db_session: AsyncSession, user_db, chat_channel) -> AsyncSession:
    channel = ChannelModel(id=1, telegram_id=chat_channel.id, title=chat_channel.title)
    channel.users.append(user_db)
    db_session.add(channel)
    await db_session.commit()
    await db_session.refresh(channel)
    return channel
