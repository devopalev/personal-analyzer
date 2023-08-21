import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base import Base


association_users_channels_table = sa.Table(
    "association_users_channels",
    Base.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("channel_id", sa.ForeignKey("telegram_channels.id", ondelete="CASCADE"), primary_key=True),
)


class TelegramChannel(Base):
    __tablename__ = "telegram_channels"

    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)

    telegram_id = sa.Column(sa.Integer, nullable=False, unique=True)
    title = sa.Column(sa.String)

    users = relationship(
        "User", secondary=association_users_channels_table, back_populates="channels", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"TelegramChannel(telegram_id={self.telegram_id}, title={self.title})"

    def __str__(self) -> str:
        return self.__repr__()
