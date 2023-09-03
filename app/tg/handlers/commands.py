import logging

from telegram import Update

from app.crud import crud_user
from app.tg.messages.menu import MessageParamsMainMenu
from app.tg.messages.others import MassageCommandHelp
from app.tg.messages.others import MassageCommandStart

logger = logging.getLogger(__name__)


async def start_handler(update: Update, *args):
    from_user = update.effective_user
    user_db = await crud_user.get_or_create(
        language_code=from_user.language_code,
        telegram_id=from_user.id,
        username=from_user.username,
        fullname=from_user.full_name,
    )
    msg = await MassageCommandStart.async_build(language_code=user_db.language_code)
    await crud_user.activate_user(user_db)
    await from_user.send_message(**msg)


async def help_handler(update: Update, *args):
    from_user = update.effective_user
    user_db = await crud_user.get_by_telegram_id(
        telegram_id=from_user.id,
    )
    msg = await MassageCommandHelp.async_build(language_code=user_db.language_code)
    await from_user.send_message(**msg)


async def main_menu_handler(update: Update, *args):
    from_user = update.effective_user
    user_db = await crud_user.get_by_telegram_id(telegram_id=from_user.id)

    msg = await MessageParamsMainMenu.async_build(language_code=user_db.language_code)
    await update.effective_message.delete()
    await from_user.send_message(**msg)
