from telegram import BotCommand
from telegram.ext import ChatMemberHandler, CommandHandler, BaseHandler

from app.tg.handlers.others import start_handler
from app.tg.handlers.others import unknown_handler, UnknownHandler

from app.tg.handlers.chat_members import chat_member_bot_handler
from app.tg.handlers.chat_members import chat_member_user_handler


def build_handlers() -> list[BaseHandler]:
    handlers = [CommandHandler("start", start_handler),
                ChatMemberHandler(chat_member_bot_handler, ChatMemberHandler.MY_CHAT_MEMBER),
                ChatMemberHandler(chat_member_user_handler, ChatMemberHandler.CHAT_MEMBER),
                UnknownHandler(unknown_handler)]

    return handlers


def build_commands() -> list[BotCommand]:
    commands = [BotCommand("start", "registration user in bot")]
    return commands


