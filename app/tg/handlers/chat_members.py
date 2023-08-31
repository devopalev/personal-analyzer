from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import CallbackContext

from app.crud import crud_channel
from app.crud import crud_user
from app.db.session import session_wrapper
from app.tg.messages.base import MessageTextBaseBuilder
from app.tg.messages.chat_members import MessageBotLeftChannel
from app.tg.messages.chat_members import MessageEventJoinedUser
from app.tg.messages.chat_members import MessageEventLeftUser

STATUS_JOIN = [
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.ADMINISTRATOR,
]
STATUS_LEFT = [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]


@session_wrapper
async def chat_member_bot_handler(
    update: Update, context: CallbackContext, session: AsyncSession
):
    new_chat_member = update.my_chat_member.new_chat_member
    old_chat_member = update.my_chat_member.old_chat_member

    from_user = update.my_chat_member.from_user
    chat = update.my_chat_member.chat

    channel_db = await crud_channel.get_or_create(
        telegram_id=chat.id, title=chat.title, session=session
    )

    if not from_user.is_bot:
        user_db = await crud_user.get_or_create(
            language_code=from_user.language_code,
            telegram_id=from_user.id,
            username=from_user.username,
            fullname=from_user.full_name,
            session=session,
        )
        if (
            new_chat_member.status == ChatMemberStatus.ADMINISTRATOR
            and old_chat_member.status != ChatMemberStatus.ADMINISTRATOR
        ):
            await crud_channel.add_associate_to_user(
                channel=channel_db, user=user_db, session=session
            )

    if (
        new_chat_member.status in STATUS_LEFT
        and old_chat_member.status not in STATUS_LEFT
    ):
        for user in channel_db.users:
            msg_text = await MessageBotLeftChannel.a_build(
                channel_db.title, user.language_code
            )
            await context.bot.send_message(
                user.telegram_id, str(msg_text), parse_mode=msg_text.PARSE_MODE
            )

        await crud_channel.delete(db_obj=channel_db, session=session)


async def chat_member_user_handler(update: Update, context: CallbackContext):
    new_chat_member = update.chat_member.new_chat_member
    old_chat_member = update.chat_member.old_chat_member
    from_user = update.chat_member.from_user
    chat = update.chat_member.chat

    channel_db = await crud_channel.get_by_telegram_id(telegram_id=chat.id)

    msg_class: Type[MessageTextBaseBuilder] = None

    # Join
    if (
        new_chat_member.status in STATUS_JOIN
        and old_chat_member.status not in STATUS_JOIN
    ):
        msg_class = MessageEventJoinedUser

    # Left
    elif (
        new_chat_member.status in STATUS_LEFT
        and old_chat_member.status not in STATUS_LEFT
    ):
        msg_class = MessageEventLeftUser

    if channel_db and msg_class:
        for user in channel_db.users:
            msg_text = await msg_class.a_build(
                from_user, channel_db.title, user.language_code
            )
            await context.bot.send_message(
                user.telegram_id, str(msg_text), parse_mode=msg_text.PARSE_MODE
            )
