from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db import ConstantsLanguageCode
from app.db import LanguageObject
from app.db import session_wrapper


class CRUDLanguageObject(CRUDBase[LanguageObject]):
    @session_wrapper
    async def get_language_codes(self, session: AsyncSession = None):
        sql = select(self.Model.language_code).distinct(self.Model.language_code)
        result = await session.execute(sql)
        return [t[0] for t in result.all()]

    @session_wrapper
    async def get(
        self,
        key: str,
        language_code: str = ConstantsLanguageCode.DEFAULT.value,
        session: AsyncSession = None,
    ) -> LanguageObject | str:
        sql = select(self.Model).where(self.Model.key == key)
        db_obj = await session.scalar(
            sql.where(self.Model.language_code == language_code)
        )

        if db_obj:
            return db_obj

        default_db_obj = await session.scalar(
            sql.where(self.Model.language_code == ConstantsLanguageCode.DEFAULT.value)
        )

        return (
            default_db_obj
            or "An error has occurred! The text for this message was not found :("
        )


crud_language = CRUDLanguageObject(LanguageObject)
