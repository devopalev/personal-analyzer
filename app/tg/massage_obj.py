from abc import ABC, abstractmethod

from telegram import User
from telegram.helpers import escape_markdown, mention_markdown
from telegram.constants import ParseMode

from app.crud import crud_language


class MessageTextBase(ABC):
    key = ""
    PARSE_MODE = ParseMode.MARKDOWN

    @abstractmethod
    def __init__(self):
        raise NotImplemented()

    @abstractmethod
    def __str__(self):
        raise NotImplemented()


class MessageEventJoinedUser(MessageTextBase):
    key = "/event/channel/joined_user"
    PARSE_MODE = ParseMode.MARKDOWN

    def __init__(self, raw_text, joined_user: User, channel_title: str):
        user_link = mention_markdown(joined_user.id, joined_user.full_name)
        self.text = raw_text.format(user_link=user_link, channel_title=channel_title)

    def __str__(self):
        return self.text

    @classmethod
    async def a_build(cls, joined_user: User, channel_title: str, language_code: str):
        text_db_obj = await crud_language.get(key=cls.key, language_code=language_code)
        raw_text: str = text_db_obj.value
        return cls(raw_text, joined_user, channel_title)


class MessageEventLeftUser(MessageEventJoinedUser):
    key = "/event/channel/left_user"
