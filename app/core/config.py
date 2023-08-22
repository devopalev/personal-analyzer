from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_NAME: str = "Personal Bot Analyzer"
    BOT_DESCRIPTION: str = "I help to run a personal channels"

    DATABASE_URI: str

    LOG_FORMAT: str = "%(asctime)s :: %(levelname)-7s :: %(name)-30s >>> %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
