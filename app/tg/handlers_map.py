from telegram import BotCommand
from telegram.ext import BaseHandler
from telegram.ext import ChatMemberHandler
from telegram.ext import CommandHandler

from app.tg.handlers.chat_members import chat_member_bot_handler
from app.tg.handlers.chat_members import chat_member_user_handler
from app.tg.handlers.others import help_handler
from app.tg.handlers.others import start_handler
from app.tg.handlers.others import unknown_handler
from app.tg.handlers.others import UnknownHandler


def build_handlers() -> list[BaseHandler]:
    handlers = [
        CommandHandler("start", start_handler),
        CommandHandler("help", help_handler),
        ChatMemberHandler(chat_member_bot_handler, ChatMemberHandler.MY_CHAT_MEMBER),
        ChatMemberHandler(chat_member_user_handler, ChatMemberHandler.CHAT_MEMBER),
        UnknownHandler(unknown_handler),
    ]

    return handlers


def build_commands() -> list[BotCommand]:
    commands = [
        BotCommand("start", "registration user in bot"),
        BotCommand("help", "detailed information about the features"),
    ]
    return commands
