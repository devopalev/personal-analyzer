import asyncio

from telegram import Update
from telegram.ext import ApplicationBuilder

from app.core import settings
from app.core.log import init_logging
from app.tg import build_handlers
from app.tg import build_commands
from app.tg import error_handler


async def main():
    init_logging()
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    commands = build_commands()
    await application.bot.set_my_commands(commands)

    handlers = build_handlers()
    application.add_handlers(handlers)
    application.add_error_handler(error_handler)

    async with application:  # Calls `initialize` and `shutdown`
        await application.start()
        # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

        await asyncio.Future()  # endless waiting


if __name__ == '__main__':
    asyncio.run(main())
