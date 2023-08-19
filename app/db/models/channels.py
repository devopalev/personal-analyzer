import sqlalchemy as sa

from app.db.base import Base


class TelegramChannel(Base):

    __tablename__ = "telegram_channels"

    telegram_id = sa.Column(sa.Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Algorithm(telegram_id={self.telegram_id})"

    def __str__(self) -> str:
        return self.__repr__()
