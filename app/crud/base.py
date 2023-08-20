from typing import TypeVar, Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base, get_async_session


ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, Model: Type[ModelType]):
        self.Model = Model
        self._get_session = get_async_session

    async def get(self) -> ModelType:
        pass

    async def create(
            self,
            **kwargs,
    ) -> ModelType:
        db = await self._get_session()
        db_obj = self.Model(**kwargs)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, ) -> ModelType:
        pass

    async def delete(self) -> bool:
        pass
