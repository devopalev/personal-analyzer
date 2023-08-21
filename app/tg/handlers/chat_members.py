from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update
from telegram.ext import CallbackContext, BaseHandler, Application, ChatMemberHandler

from telegram.constants import ChatMemberStatus

from app.db.session import session_wrapper
from app.crud import crud_user
from app.crud import crud_channel

from app.tg.messages.chat_members import MessageEventJoinedUser, MessageEventLeftUser, MessageTextBase

STATUS_JOIN = [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.ADMINISTRATOR]
STATUS_LEFT = [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]


@session_wrapper
async def chat_member_bot(update: Update, context: CallbackContext, session: AsyncSession):
    new_chat_member = update.my_chat_member.new_chat_member
    old_chat_member = update.my_chat_member.old_chat_member

    from_user = update.my_chat_member.from_user
    chat = update.my_chat_member.chat

    user_db = await crud_user.get_by_telegram_id(telegram_id=from_user.id, session=session)
    if not user_db:
        user_db = await crud_user.create(language_code=from_user.language_code, telegram_id=from_user.id,
                                         username=from_user.username, fullname=from_user.full_name,
                                         session=session)

    channel_db = await crud_channel.get_by_telegram_id(telegram_id=chat.id, session=session)
    if not channel_db:
        channel_db = await crud_channel.create(telegram_id=chat.id, title=chat.title, session=session)

    if (new_chat_member.status == ChatMemberStatus.ADMINISTRATOR and
            old_chat_member.status != ChatMemberStatus.ADMINISTRATOR):
        await crud_channel.add_associate_to_user(channel=channel_db, user=user_db, session=session)

    elif new_chat_member.status in STATUS_LEFT and old_chat_member.status not in STATUS_LEFT:
        users = channel_db.users
        await crud_channel.delete(db_obj=channel_db, session=session)

        for user in users:
            pass  # TODO: сообщение что бот удалён из канала


async def chat_member_user(update: Update, context: CallbackContext):
    new_chat_member = update.chat_member.new_chat_member
    old_chat_member = update.chat_member.old_chat_member
    from_user = update.chat_member.from_user
    chat = update.chat_member.chat

    channel_db = await crud_channel.get_by_telegram_id(telegram_id=chat.id)

    msg_class: MessageTextBase = None

    # Join
    if new_chat_member.status in STATUS_JOIN and old_chat_member.status not in STATUS_JOIN:
        msg_class = MessageEventJoinedUser

    # Left
    elif new_chat_member.status in STATUS_LEFT and old_chat_member.status not in STATUS_LEFT:
        msg_class = MessageEventLeftUser

    if channel_db and msg_class:
        for user in channel_db.users:
            msg_text = await msg_class.a_build(from_user, channel_db.title, user.language_code)
            await context.bot.send_message(user.telegram_id, str(msg_text), parse_mode=msg_text.PARSE_MODE)


def registration_chat_members_handlers(app: Application):
    app.add_handler(ChatMemberHandler(chat_member_bot, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(ChatMemberHandler(chat_member_user, ChatMemberHandler.CHAT_MEMBER))
