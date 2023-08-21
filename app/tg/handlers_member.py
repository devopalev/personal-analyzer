from sqlalchemy.ext.asyncio import AsyncSession
from telegram import Update, ChatMember
from telegram.ext import CallbackContext, BaseHandler, ChatJoinRequestHandler, ChatMemberHandler

from telegram.constants import ChatMemberStatus

from app.db.session import session_wrapper
from app.crud import crud_user
from app.crud import crud_channel

from app.tg.massage_obj import MessageEventJoinedUser, MessageEventLeftUser

STATUS_JOIN = [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.ADMINISTRATOR]
STATUS_LEFT = [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]


@session_wrapper
async def chat_member_bot(update: Update, context: CallbackContext, session: AsyncSession):
    new_chat_member = update.my_chat_member.new_chat_member
    old_chat_member = update.my_chat_member.old_chat_member

    if (new_chat_member.status == ChatMemberStatus.ADMINISTRATOR and
            old_chat_member.status != ChatMemberStatus.ADMINISTRATOR):
        print("New chat", update.to_dict())

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

        await crud_channel.associate_to_user(channel=channel_db, user=user_db, session=session)

    elif new_chat_member.status in STATUS_LEFT and old_chat_member.status not in STATUS_LEFT:
        print('Left the chat', update.to_dict())


async def chat_member_user(update: Update, context: CallbackContext):
    new_chat_member = update.chat_member.new_chat_member
    old_chat_member = update.chat_member.old_chat_member
    from_user = update.chat_member.from_user
    chat = update.chat_member.chat

    channel_db = await crud_channel.get_by_telegram_id(telegram_id=chat.id)

    if channel_db:
        for user in channel_db.users:

            # Join
            if new_chat_member.status in STATUS_JOIN and old_chat_member.status not in STATUS_JOIN:
                msg_text = await MessageEventJoinedUser.a_build(from_user, channel_db.title, user.language_code)
                await context.bot.send_message(user.telegram_id, str(msg_text), parse_mode=msg_text.PARSE_MODE)

            # Left
            elif new_chat_member.status in STATUS_LEFT and old_chat_member.status not in STATUS_LEFT:
                msg_text = await MessageEventLeftUser.a_build(from_user, channel_db.title, user.language_code)
                await context.bot.send_message(user.telegram_id, str(msg_text), parse_mode=msg_text.PARSE_MODE)


async def chat_join(update: Update, context: CallbackContext):
    print('Join HANDLER', update.to_dict())


class UnknownHandler(BaseHandler):
    def check_update(self, *args, **kwargs):
        return True


async def unknown_handler(update: Update, context: CallbackContext):
    print("Unknown update", update.to_dict())
