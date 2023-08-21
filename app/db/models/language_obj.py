from enum import StrEnum

import sqlalchemy as sa

from app.db.base import Base


class ConstantsLanguageCode(StrEnum):
    RU = "ru"
    EN = "en"

    DEFAULT = RU


class LanguageObject(Base):

    __tablename__ = "language_objects"

    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)

    language_code = sa.Column(sa.String, nullable=False)
    key = sa.Column(sa.String, nullable=False)
    value = sa.Column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f"Algorithm(telegram_id={self})"

    def __str__(self) -> str:
        return self.__repr__()
