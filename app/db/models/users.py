import sqlalchemy as sa

from app.db.base import Base


#TODO: докинуть username и тд
class User(Base):
    class ModelConstants:
        ROLE_ROOT = "root"
        ROLE_ADMIN = "admin"
        ROLE_USER = "user"

    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True, autoincrement=True)

    telegram_id = sa.Column(sa.Integer, nullable=False, unique=True)
    role = sa.Column(sa.String, default=ModelConstants.ROLE_USER, nullable=False)  # root, admin, user
    language = sa.Column(sa.String, default="ru")
    active = sa.Column(sa.Boolean, default=False)

    def __repr__(self) -> str:
        return f"User(telegram_id={self.telegram_id})"

    def __str__(self) -> str:
        return self.__repr__()
