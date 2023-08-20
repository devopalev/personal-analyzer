import asyncio
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, Application
from telegram.error import RetryAfter


from app.core import settings
from app.tg.handlers_member import *
from app.crud import crud_user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


async def preconfiguring_bot(application: Application):
    """
    Pre-configuring the bot. Installing the logo, description, etc

    """
    try:
        if await application.bot.get_my_name() != settings.BOT_NAME:
            await application.bot.set_my_name(name=settings.BOT_NAME)

        if await application.bot.get_my_description() != settings.BOT_DESCRIPTION:
            await application.bot.set_my_description(description=settings.BOT_DESCRIPTION)
    except RetryAfter:
        pass


async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")




async def main():
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.add_handler(ChatJoinRequestHandler(chat_join))
    # Keep track of which chats the bot is in
    application.add_handler(ChatMemberHandler(chat_member_bot, ChatMemberHandler.MY_CHAT_MEMBER))

    # Handle members joining/leaving chats
    application.add_handler(ChatMemberHandler(chat_member_user, ChatMemberHandler.CHAT_MEMBER))

    application.add_handler(UnknownHandler(unknown_handler))

    await preconfiguring_bot(application)

    async with application:  # Calls `initialize` and `shutdown`
        await application.start()
        # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

        await asyncio.Future()  # endless waiting


if __name__ == '__main__':
    asyncio.run(main())