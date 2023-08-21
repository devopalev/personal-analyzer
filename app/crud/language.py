from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db import LanguageObject, session_wrapper


class CRUDLanguageObject(CRUDBase[LanguageObject]):
    @session_wrapper
    async def get(self, key: str, language_code: str, session: AsyncSession = None) -> LanguageObject:
        sql = select(self.Model).where(self.Model.key == key, self.Model.language_code == language_code)
        db_obj = await session.scalar(sql)
        return db_obj


crud_language = CRUDLanguageObject(LanguageObject)
