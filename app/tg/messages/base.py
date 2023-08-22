from abc import ABC, abstractmethod

from telegram.constants import ParseMode


class MessageTextBase(ABC):
    key = ""
    PARSE_MODE = ParseMode.MARKDOWN

    @abstractmethod
    def __init__(self):
        raise NotImplemented()

    @abstractmethod
    def __str__(self):
        raise NotImplemented()


class MessageTextBaseBuilder(MessageTextBase):
    @classmethod
    @abstractmethod
    async def a_build(cls, *args, **kwargs):
        raise NotImplemented()
