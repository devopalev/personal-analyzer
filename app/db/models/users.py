import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    telegram_id = sa.Column(sa.Integer, nullable=False)
    role = sa.Column(sa.String)  # root, admin, user
    language = sa.Column(sa.String)

    def __repr__(self) -> str:
        return f"Algorithm(telegram_id={self.telegram_id})"

    def __str__(self) -> str:
        return self.__repr__()
