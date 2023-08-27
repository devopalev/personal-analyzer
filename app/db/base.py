import subprocess

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from app.core.exceptions import AlembicException

Base: DeclarativeMeta = declarative_base()


def init_db():
    response = subprocess.run(["alembic", "upgrade", "head"])
    if response.returncode != 0:
        raise AlembicException("Migration failure.")
