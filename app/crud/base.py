from typing import TypeVar, Generic, Type

from app.db import Base


ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, Model: Type[ModelType]):
        self.Model = Model

    async def get(self) -> ModelType:
        pass

    async def create(self) -> ModelType:
        pass

    async def update(self) -> ModelType:
        pass

    async def delete(self) -> bool:
        pass
