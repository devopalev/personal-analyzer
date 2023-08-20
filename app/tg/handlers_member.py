from telegram import Update, ChatMember
from telegram.ext import CallbackContext, BaseHandler, ChatJoinRequestHandler, ChatMemberHandler

from telegram.constants import ChatMemberStatus


from app.crud import crud_user


STATUS_JOIN = [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.ADMINISTRATOR]
STATUS_LEFT = [ChatMemberStatus.BANNED, ChatMemberStatus.LEFT]


async def chat_member_bot(update: Update, context: CallbackContext):
    new_chat_member = update.my_chat_member.new_chat_member
    old_chat_member = update.my_chat_member.old_chat_member

    if (new_chat_member.status == ChatMemberStatus.ADMINISTRATOR and
            old_chat_member.status != ChatMemberStatus.ADMINISTRATOR):
        print("New chat", update.to_dict())
        user = new_chat_member.user
        user_db = await crud_user.get_by_telegram_id(telegram_id=user.id)
        if not user_db:
            user_db = await crud_user.create(telegram_id=user.id)
        print(user_db)


    elif new_chat_member.status in STATUS_LEFT and old_chat_member.status not in STATUS_LEFT:
        print('Left the chat', update.to_dict())


async def chat_member_user(update: Update, context: CallbackContext):
    new_chat_member = update.my_chat_member.new_chat_member
    old_chat_member = update.my_chat_member.old_chat_member

    # Join
    if new_chat_member.status in STATUS_JOIN and old_chat_member.status not in STATUS_JOIN:
        pass

    # Left
    if new_chat_member.status in STATUS_LEFT and old_chat_member.status not in STATUS_LEFT:
        pass

    print('User Member HANDLER', update.to_dict())


async def chat_join(update: Update, context: CallbackContext):
    print('Join HANDLER', update.to_dict())


class UnknownHandler(BaseHandler):
    def check_update(self, *args, **kwargs):
        return True


async def unknown_handler(update: Update, context: CallbackContext):
    print("Unknown update", update.to_dict())
