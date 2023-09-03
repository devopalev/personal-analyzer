import subprocess

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AlembicException
from app.db.session import session_wrapper


@session_wrapper
async def init_db(session: AsyncSession = None):
    response = subprocess.run(["alembic", "upgrade", "head"])
    if response.returncode != 0:
        raise AlembicException("Migration failure.")

    with open("app/static/language_objects.sql", "r", encoding="utf-8") as file:
        dump = file.read()

    await session.execute(text(dump))
    await session.commit()
