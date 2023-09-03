import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Chat
from telegram import ChatMemberAdministrator
from telegram import ChatMemberBanned
from telegram import ChatMemberMember
from telegram import ChatMemberUpdated
from telegram import Update

from app.db.models.channels import TelegramChannel as ChannelModel
from app.db.models.users import User as UserModel
from app.tg.handlers.chat_members import chat_member_bot_handler
from app.tg.handlers.chat_members import chat_member_user_handler
from app.tg.messages.chat_members import MessageBotLeftChannel
from app.tg.messages.chat_members import MessageEventJoinedUser
from app.tg.messages.chat_members import MessageEventLeftUser


@pytest.mark.asyncio
async def test_chat_member_bot_handler(
    db_session: AsyncSession,
    chat_channel: Chat,
    user_test,
    context,
    user_bot_test,
    curr_datetime_utc,
):
    # Common obj
    chat_member_administrator = ChatMemberAdministrator(
        api_kwargs={"can_manage_voice_chats": True},
        can_be_edited=False,
        can_change_info=True,
        can_delete_messages=True,
        can_edit_messages=True,
        can_invite_users=True,
        can_manage_chat=True,
        can_manage_video_chats=True,
        can_post_messages=True,
        can_promote_members=False,
        can_restrict_members=True,
        is_anonymous=False,
        user=user_bot_test,
    )
    chat_member_banned = ChatMemberBanned(
        until_date=curr_datetime_utc, user=user_bot_test
    )

    # Join
    cmu_join = ChatMemberUpdated(
        chat=chat_channel,
        date=curr_datetime_utc,
        new_chat_member=chat_member_administrator,
        old_chat_member=chat_member_banned,
        from_user=user_test,
    )

    update_join = Update(my_chat_member=cmu_join, update_id=2)

    await chat_member_bot_handler(update_join, context)

    user_db = await db_session.get(UserModel, 1)
    assert user_db.telegram_id == user_test.id

    channel_db = await db_session.get(ChannelModel, 1)
    assert channel_db.telegram_id == chat_channel.id

    # Left
    cmu_left = ChatMemberUpdated(
        chat=chat_channel,
        date=curr_datetime_utc,
        from_user=user_test,
        new_chat_member=chat_member_banned,
        old_chat_member=chat_member_administrator,
    )
    update_left = Update(my_chat_member=cmu_left, update_id=3)

    await chat_member_bot_handler(update_left, context, session=db_session)

    channel_db = await db_session.get(ChannelModel, 1)
    assert channel_db is None

    orig_msg = await MessageBotLeftChannel.async_build(
        chat_channel.title, language_code=user_test.language_code
    )

    assert context.test_storage["text"] == orig_msg["text"]


@pytest.mark.asyncio
async def test_chat_member_user_handler(
    db_session, chat_channel, user_test, curr_datetime_utc, context, channel_db
):
    # Join
    chat_member_member = ChatMemberMember(user=user_test)

    chat_member_banned = ChatMemberBanned(until_date=curr_datetime_utc, user=user_test)

    chat_member_updated_join = ChatMemberUpdated(
        chat=chat_channel,
        date=curr_datetime_utc,
        from_user=user_test,
        new_chat_member=chat_member_member,
        old_chat_member=chat_member_banned,
    )

    update = Update(chat_member=chat_member_updated_join, update_id=4)

    await chat_member_user_handler(update, context)

    orig_msg = await MessageEventJoinedUser.async_build(
        user_test, chat_channel.title, user_test.language_code
    )

    assert context.test_storage["text"] == orig_msg["text"]

    # Left
    chat_member_updated_left = ChatMemberUpdated(
        chat=chat_channel,
        date=curr_datetime_utc,
        from_user=user_test,
        new_chat_member=chat_member_banned,
        old_chat_member=chat_member_member,
    )

    update = Update(chat_member=chat_member_updated_left, update_id=4)
    await chat_member_user_handler(update, context)

    orig_msg = await MessageEventLeftUser.async_build(
        user_test, chat_channel.title, user_test.language_code
    )

    assert context.test_storage["text"] == orig_msg["text"]
