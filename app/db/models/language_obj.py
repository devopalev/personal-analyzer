import sqlalchemy as sa

from app.db.base import Base


class LanguageObjects(Base):

    __tablename__ = "language_objects"

    language = sa.Column(sa.String, nullable=False)
    key = sa.Column(sa.String, nullable=False)
    value = sa.Column(sa.String, nullable=False)

    def __repr__(self) -> str:
        return f"Algorithm(telegram_id={self})"

    def __str__(self) -> str:
        return self.__repr__()
