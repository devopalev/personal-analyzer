import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base import Base


#TODO: докинуть username и тд
from app.db.models.channels import association_users_channels_table


class User(Base):
    class ModelConstants:
        ROLE_ROOT = "root"
        ROLE_ADMIN = "admin"
        ROLE_USER = "user"

    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)

    telegram_id = sa.Column(sa.Integer, nullable=False, unique=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    username = sa.Column(sa.String)

    role = sa.Column(sa.String, default=ModelConstants.ROLE_USER, nullable=False)
    language_code = sa.Column(sa.String, default="ru")
    active = sa.Column(sa.Boolean, default=False)

    channels = relationship(
        "TelegramChannel", secondary=association_users_channels_table, back_populates="users"
    )

    def __repr__(self) -> str:
        return f"User(telegram_id={self.telegram_id})"

    def __str__(self) -> str:
        return self.__repr__()
