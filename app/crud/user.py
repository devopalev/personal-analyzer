from app.crud.base import CRUDBase
from app.db import User
from app.db import ConstantsLanguageCode


class CRUDUser(CRUDBase[User]):
    async def create(self, **kwargs) -> User:
        language_code = kwargs.pop("language_code", ConstantsLanguageCode.DEFAULT.value)
        if language_code not in tuple(ConstantsLanguageCode):
            language_code = ConstantsLanguageCode.DEFAULT.value
        return await super().create(language_code=language_code, **kwargs)


crud_user = CRUDUser(User)
