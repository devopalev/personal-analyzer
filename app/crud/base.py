from typing import TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base, session_wrapper


ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, Model: Type[ModelType]):
        self.Model = Model

    @session_wrapper
    async def get_by_telegram_id(self, telegram_id: int, session: AsyncSession = None) -> ModelType:
        sql = select(self.Model).where(self.Model.telegram_id == telegram_id)
        db_obj = await session.scalar(sql)
        return db_obj

    @session_wrapper
    async def create(self, session: AsyncSession = None, **kwargs) -> ModelType:
        db_obj = self.Model(**kwargs)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    @session_wrapper
    async def delete(self, db_obj: ModelType, session: AsyncSession = None) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    @session_wrapper
    async def get_or_create(self, session: AsyncSession = None, **kwargs) -> ModelType:
        telegram_id = kwargs["telegram_id"]
        user_db = await self.get_by_telegram_id(telegram_id=telegram_id, session=session)
        return user_db or await self.create(session=session, **kwargs)
