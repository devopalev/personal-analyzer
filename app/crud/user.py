from sqlalchemy import select

from app.crud.base import CRUDBase
from app.db.models.users import User


class CRUDUser(CRUDBase[User]):
    pass


crud_user = CRUDUser(User)
