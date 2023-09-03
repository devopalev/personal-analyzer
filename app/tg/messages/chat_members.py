from telegram import User
from telegram.helpers import mention_markdown

from app.crud import crud_language
from app.tg.messages.base import BaseMessageParams


class MessageEventJoinedUser(BaseMessageParams):
    _key_message_text = "/event/channel/joined_user"

    @classmethod
    async def async_build(
        cls, joined_user: User, channel_title: str, language_code: str
    ):
        text_db_obj = await crud_language.get(
            key=cls._key_message_text, language_code=language_code
        )
        user_link = mention_markdown(joined_user.id, joined_user.full_name)
        text = str(text_db_obj).format(user_link=user_link, channel_title=channel_title)
        return cls(text=text)


class MessageEventLeftUser(MessageEventJoinedUser):
    _key_message_text = "/event/channel/left_user"


class MessageBotLeftChannel(BaseMessageParams):
    _key_message_text = "/event/channel/left_bot"

    @classmethod
    async def async_build(cls, channel_title: str, language_code: str):
        text_db_obj = await crud_language.get(
            key=cls._key_message_text, language_code=language_code
        )
        text = str(text_db_obj).format(channel_title=channel_title)
        return cls(text=text)
