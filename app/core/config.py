from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    BOT_NAME: str = "Personal Bot Analyzer"
    BOT_DESCRIPTION: str = "I help to run a personal channels"

    POSTGRES_HOST: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""

    LOG_FORMAT: str = "%(asctime)s :: %(levelname)-7s :: %(name)-30s >>> %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    DEBUG_MOD: bool = False

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_file_encoding="utf-8"
    )

    @property
    def database_uri(self):
        if (
            self.POSTGRES_HOST
            and self.POSTGRES_DB
            and self.POSTGRES_USER
            and self.POSTGRES_PASSWORD
        ):
            return (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}/{self.POSTGRES_DB}"
            )
        else:
            return "sqlite+aiosqlite:///database.sqlite"


settings = Settings()
