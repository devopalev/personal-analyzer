from typing import TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base, session_wrapper


ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, Model: Type[ModelType]):
        self.Model = Model

    async def get(self) -> ModelType:
        pass

    @session_wrapper
    async def get_by_telegram_id(self, telegram_id: int, session: AsyncSession = None):
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

    async def update(self) -> ModelType:
        pass

    async def delete(self) -> bool:
        pass
