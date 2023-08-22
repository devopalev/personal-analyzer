from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db import User, session_wrapper
from app.db import ConstantsLanguageCode


class CRUDUser(CRUDBase[User]):
    @session_wrapper
    async def get_or_create(self, session: AsyncSession = None, **kwargs) -> User:
        language_code = kwargs.pop("language_code", ConstantsLanguageCode.DEFAULT.value)
        if language_code not in tuple(ConstantsLanguageCode):
            language_code = ConstantsLanguageCode.DEFAULT.value
        return await super().get_or_create(language_code=language_code, session=session, **kwargs)

    @session_wrapper
    async def activate_user(self, user_obj: User, session: AsyncSession = None):
        if not user_obj.active:
            user_obj.active = True
            session.add(user_obj)
            await session.commit()


crud_user = CRUDUser(User)
