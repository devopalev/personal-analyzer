import logging

from telegram import Update

from app.crud import crud_user
from app.tg.messages.base import CallbackData
from app.tg.messages.menu import MessageParamsMenuSettings
from app.tg.messages.menu import MessageParamsSettingLanguage

logger = logging.getLogger(__name__)


async def action_handler_event_channels_setting(update: Update, *args):
    user_db = await crud_user.get_by_telegram_id(telegram_id=update.effective_user.id)
    user_db.channel_events = not user_db.channel_events
    await crud_user.update(user_db)
    await settings_handler(update, *args, user_db=user_db)


async def settings_handler(update: Update, *args, user_db=None):
    await update.callback_query.answer()
    user_db = user_db or await crud_user.get_by_telegram_id(
        telegram_id=update.effective_user.id
    )

    msg = await MessageParamsMenuSettings.async_build(
        language_code=user_db.language_code, action=not user_db.channel_events
    )
    await update.effective_message.edit_text(**msg)


async def settings_change_language_handler(update: Update, *args):
    await update.callback_query.answer()
    user_db = await crud_user.get_by_telegram_id(telegram_id=update.effective_user.id)

    msg = await MessageParamsSettingLanguage.async_build(
        language_code=user_db.language_code
    )
    await update.effective_message.edit_text(**msg)


async def settings_select_language_handler(update: Update, *args):
    await update.callback_query.answer()
    user_db = await crud_user.get_by_telegram_id(telegram_id=update.effective_user.id)

    language_code = CallbackData.build_from_callback_data(
        update.callback_query.data
    ).params["language_code"]
    user_db.language_code = language_code
    await crud_user.update(user_db)
    await settings_handler(update, *args, user_db=user_db)
