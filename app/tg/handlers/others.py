import logging

from telegram import Update, Chat
from telegram.ext import BaseHandler, CallbackContext

from app.core.log import logger_decorator
from app.crud import crud_user
from app.tg.messages.others import MassageEventError
from app.db.models.language_obj import ConstantsLanguageCode

logger = logging.getLogger(__name__)


@logger_decorator(__name__)
async def start_handler(update: Update, context: CallbackContext):
    from_user = update.effective_user
    user_db = await crud_user.get_or_create(language_code=from_user.language_code, telegram_id=from_user.id,
                                            username=from_user.username, fullname=from_user.full_name)
    await crud_user.activate_user(user_db)
    await from_user.send_message("I'm a bot, please talk to me!")


class UnknownHandler(BaseHandler):
    def check_update(self, *args, **kwargs):
        return True


async def unknown_handler(update: Update, context: CallbackContext):
    logger.warning(f"Unknown update: {update}")


async def error_handler(update: Update, context: CallbackContext):
    try:
        # don't confuse user with particular error data
        if update:
            if update.effective_chat.type == Chat.PRIVATE:
                user_db = await crud_user.get_by_telegram_id(telegram_id=update.effective_user.id)
                if user_db:
                    msg_text = MassageEventError.a_build(language_code=user_db.language_code)
                    await update.effective_user.send_message(str(msg_text))
            elif update.effective_chat.type in (Chat.GROUP, Chat.SUPERGROUP):
                msg_text = MassageEventError.a_build(language_code=ConstantsLanguageCode.DEFAULT)
                await update.effective_chat.send_message(str(msg_text))
    except Exception as e:
        logger.error("Send error message failed", exc_info=e)
