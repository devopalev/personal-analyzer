from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.db.models.channels import TelegramChannel
from app.db.models.users import User


class CRUDTelegramChannel(CRUDBase[TelegramChannel]):
    @staticmethod
    async def add_associate_to_user(
        channel: TelegramChannel, user: User, session: AsyncSession = None
    ) -> TelegramChannel:
        channel.users.append(user)
        session.add(channel)
        await session.commit()
        return channel


crud_channel = CRUDTelegramChannel(TelegramChannel)
