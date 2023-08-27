import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Message
from telegram import MessageEntity
from telegram import Update
from telegram.constants import MessageEntityType

from app.db.models.users import User
from app.tg.handlers.others import help_handler
from app.tg.handlers.others import start_handler
from app.tg.messages.others import MassageCommandHelp
from app.tg.messages.others import MassageCommandStart


@pytest.mark.asyncio
async def test_start_handler(
    db_session: AsyncSession, chat_private, user_test, curr_datetime_utc
):
    message_entity = MessageEntity(
        length=6, offset=0, type=MessageEntityType.BOT_COMMAND
    )

    message = Message(
        channel_chat_created=False,
        chat=chat_private,
        date=curr_datetime_utc,
        delete_chat_photo=False,
        entities=(message_entity,),
        from_user=user_test,
        group_chat_created=False,
        message_id=95,
        supergroup_chat_created=False,
        text="/start",
    )

    update = Update(message=message, update_id=123456789)
    await start_handler(update, None)

    res = await db_session.get(User, 1)
    assert res.telegram_id == user_test.id

    orig_msg = str(
        await MassageCommandStart.a_build(language_code=user_test.language_code)
    )
    assert user_test.test_storage["send_message"] == orig_msg


@pytest.mark.asyncio
async def test_help_handler(chat_private, user_test, curr_datetime_utc, user_db):
    message_entity = MessageEntity(
        length=6, offset=0, type=MessageEntityType.BOT_COMMAND
    )

    message = Message(
        channel_chat_created=False,
        chat=chat_private,
        date=curr_datetime_utc,
        delete_chat_photo=False,
        entities=(message_entity,),
        from_user=user_test,
        group_chat_created=False,
        message_id=95,
        supergroup_chat_created=False,
        text="/help",
    )

    update = Update(message=message, update_id=123456789)
    await help_handler(update, None)

    orig_msg = str(
        await MassageCommandHelp.a_build(language_code=user_test.language_code)
    )
    assert user_test.test_storage["send_message"] == orig_msg
