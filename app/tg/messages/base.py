from abc import ABC
from abc import abstractmethod

from telegram.constants import ParseMode

from app.crud import crud_language


class MessageTextBase(ABC):
    key = "/example/example_key"
    PARSE_MODE = ParseMode.MARKDOWN

    @abstractmethod
    def __init__(self):
        raise NotImplementedError()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()


class MessageTextBaseBuilder(MessageTextBase):
    @classmethod
    @abstractmethod
    async def a_build(cls, *args, **kwargs):
        raise NotImplementedError()


class MessageTextSimpleBuilder(MessageTextBaseBuilder):
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text

    @classmethod
    async def a_build(cls, language_code: str = None):
        text_db_obj = await crud_language.get(key=cls.key, language_code=language_code)
        return cls(str(text_db_obj))
