from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db import ConstantsLanguageCode
from app.db import LanguageObject
from app.db import session_wrapper


class CRUDLanguageObject(CRUDBase[LanguageObject]):
    @session_wrapper
    async def get(
        self,
        key: str,
        language_code: str = ConstantsLanguageCode.DEFAULT.value,
        session: AsyncSession = None,
    ) -> LanguageObject | str:
        if language_code not in tuple(ConstantsLanguageCode):
            language_code = ConstantsLanguageCode.DEFAULT.value
        sql = select(self.Model).where(
            self.Model.key == key, self.Model.language_code == language_code
        )
        db_obj = await session.scalar(sql)
        return (
            db_obj
            or "An error has occurred! The text for this message was not found :("
        )


crud_language = CRUDLanguageObject(LanguageObject)
