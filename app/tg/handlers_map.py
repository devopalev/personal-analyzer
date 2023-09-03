from telegram import BotCommand
from telegram.ext import BaseHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import ChatMemberHandler
from telegram.ext import CommandHandler

from app.tg.handlers.chat_members import chat_member_bot_handler
from app.tg.handlers.chat_members import chat_member_user_handler
from app.tg.handlers.commands import help_handler
from app.tg.handlers.commands import main_menu_handler
from app.tg.handlers.commands import start_handler
from app.tg.handlers.menu import action_handler_event_channels_setting
from app.tg.handlers.menu import settings_change_language_handler
from app.tg.handlers.menu import settings_handler
from app.tg.handlers.menu import settings_select_language_handler
from app.tg.handlers.others import close_message
from app.tg.handlers.others import unknown_handler
from app.tg.handlers.others import UnknownHandler
from app.tg.messages.base import factory_btn_close
from app.tg.messages.menu import MessageParamsMainMenu
from app.tg.messages.menu import MessageParamsMenuSettings
from app.tg.messages.menu import MessageParamsSettingLanguage


def build_handlers() -> list[BaseHandler]:
    handlers = [
        CommandHandler("start", start_handler),
        CommandHandler("help", help_handler),
        # Main menu
        CommandHandler("menu", main_menu_handler),
        CallbackQueryHandler(
            main_menu_handler,
            MessageParamsMainMenu.callback_entry.re_strict_callback_data,
        ),
        # Member handles
        ChatMemberHandler(chat_member_bot_handler, ChatMemberHandler.MY_CHAT_MEMBER),
        ChatMemberHandler(chat_member_user_handler, ChatMemberHandler.CHAT_MEMBER),
        # Settings handles
        CallbackQueryHandler(
            settings_handler,
            MessageParamsMainMenu.factory_settings_btn.callback_data.re_strict_callback_data,
        ),
        CallbackQueryHandler(
            action_handler_event_channels_setting,
            MessageParamsMenuSettings.factory_btn_event_enable.callback_data.re_strict_callback_data,
        ),
        CallbackQueryHandler(
            settings_change_language_handler,
            MessageParamsMenuSettings.factory_btn_language.callback_data.re_strict_callback_data,
        ),
        CallbackQueryHandler(
            settings_select_language_handler,
            MessageParamsSettingLanguage.factory_buttons_language.callback_data.re_callback_data,
        ),
        # Other
        CallbackQueryHandler(
            close_message, factory_btn_close.callback_data.re_strict_callback_data
        ),
        # Unknown handler must always be the last
        UnknownHandler(unknown_handler),
    ]

    return handlers


def build_commands() -> list[BotCommand]:
    commands = [
        BotCommand("start", "registration user in bot"),
        BotCommand("help", "detailed information about the features"),
        BotCommand("menu", "main menu"),
    ]
    return commands
