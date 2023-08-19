import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, Application


from app.core import settings


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# logging.getLogger("httpx").setLevel(logging.WARNING)


async def preconfiguring_bot(application: Application):
    """
    Pre-configuring the bot. Installing the logo, description, etc

    """

    if await application.bot.get_my_name() != settings.BOT_NAME:
        await application.bot.set_my_name(settings.BOT_NAME)

    if await application.bot.get_my_description() != settings.BOT_DESCRIPTION:
        await application.bot.set_my_description(settings.BOT_DESCRIPTION)


async def start(update: Update, context: CallbackContext):
    pass
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def main():
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    await preconfiguring_bot(application)

    async with application:  # Calls `initialize` and `shutdown`
        await application.start()
        await application.updater.start_polling()

        await asyncio.Future()  # endless waiting


if __name__ == '__main__':
    asyncio.run(main())