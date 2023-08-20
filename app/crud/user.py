from sqlalchemy import select

from app.crud.base import CRUDBase
from app.db.models.users import User


class CRUDUser(CRUDBase[User]):
    async def get_by_telegram_id(self, telegram_id: int):
        db = await self._get_session()
        sql = select(self.Model).where(self.Model.telegram_id == telegram_id)
        db_obj = await db.scalar(sql)
        return db_obj


crud_user = CRUDUser(User)
