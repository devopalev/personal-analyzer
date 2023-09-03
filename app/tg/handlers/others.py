import logging

from telegram import Chat
from telegram import Update
from telegram.ext import BaseHandler
from telegram.ext import CallbackContext

from app.crud import crud_user
from app.db.models.language_obj import ConstantsLanguageCode
from app.tg.messages.others import MassageEventError

logger = logging.getLogger(__name__)


class UnknownHandler(BaseHandler):
    def check_update(self, *args, **kwargs):
        return True


async def unknown_handler(update: Update, *args):
    logger.warning(f"Unknown update: {update}")

    if update.callback_query:
        await update.callback_query.answer("Unknown action")


async def error_handler(update: Update, context: CallbackContext):
    logger.error("Exception while handling an update:", exc_info=context.error)

    try:
        # don't confuse user with particular error data
        if update:
            if update.effective_chat.type == Chat.PRIVATE:
                user_db = await crud_user.get_by_telegram_id(
                    telegram_id=update.effective_user.id
                )
                if user_db:
                    msg = await MassageEventError.async_build(
                        language_code=user_db.language_code
                    )
                    await update.effective_user.send_message(**msg)
            elif update.effective_chat.type in (Chat.GROUP, Chat.SUPERGROUP):
                msg = await MassageEventError.async_build(
                    language_code=ConstantsLanguageCode.DEFAULT
                )
                await update.effective_chat.send_message(**msg)
    except Exception as e:
        logger.error("Send error message failed", exc_info=e)


async def close_message(update: Update, *args):
    await update.effective_message.delete()
