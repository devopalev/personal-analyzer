from app.crud import crud_language
from app.tg.messages.base import MessageTextBaseBuilder


class MassageEventError(MessageTextBaseBuilder):
    key = "/event/error"

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    @classmethod
    async def a_build(cls, language_code: str = None):
        text_db_obj = await crud_language.get(key=cls.key, language_code=language_code)
        return cls(str(text_db_obj))


class MassageCommandStart(MessageTextBaseBuilder):
    key = "/commands/start"

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    @classmethod
    async def a_build(cls, language_code: str = None):
        text_db_obj = await crud_language.get(key=cls.key, language_code=language_code)
        return cls(str(text_db_obj))
