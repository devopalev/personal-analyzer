from telegram import User
from telegram.helpers import mention_markdown
from telegram.constants import ParseMode

from app.crud import crud_language
from app.tg.messages.base import MessageTextBaseBuilder


class MessageEventJoinedUser(MessageTextBaseBuilder):
    key = "/event/channel/joined_user"
    PARSE_MODE = ParseMode.MARKDOWN

    def __init__(self, raw_text: str, joined_user: User, channel_title: str):
        user_link = mention_markdown(joined_user.id, joined_user.full_name)
        self.text = raw_text.format(user_link=user_link, channel_title=channel_title)

    def __str__(self):
        return self.text

    @classmethod
    async def a_build(cls, joined_user: User, channel_title: str, language_code: str):
        text_db_obj = await crud_language.get(key=cls.key, language_code=language_code)
        return cls(str(text_db_obj), joined_user, channel_title)


class MessageEventLeftUser(MessageEventJoinedUser):
    key = "/event/channel/left_user"


class MessageBotLeftChannel(MessageTextBaseBuilder):
    key = "/event/channel/left_bot"

    def __init__(self, raw_text: str, channel_title: str):
        self.text = raw_text.format(channel_title=channel_title)

    def __str__(self):
        return self.text

    @classmethod
    async def a_build(cls, channel_title: str, language_code: str):
        text_db_obj = await crud_language.get(key=cls.key, language_code=language_code)
        return cls(str(text_db_obj), channel_title)
