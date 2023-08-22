import logging
from functools import wraps
from typing import Callable

from telegram import Update


from app.core.config import settings


def logger_decorator(logger_name: str):
    def outer_wrapper(function: Callable) -> Callable:
        @wraps(function)
        async def inner_wrapper(*args, **kwargs) -> Callable:
            logger = logging.getLogger(logger_name)

            extra_log_info = f"[logger_decorator] [function({function.__name__})] "

            if args and isinstance(args[0], Update):
                update = args[0]
                username = update.effective_user.username
                user_id = update.effective_user.id
                logger.debug(extra_log_info + f"{username}({user_id}): {update}")
            else:
                logger.debug(extra_log_info + str(args) + str(kwargs))
            try:
                return await function(*args, **kwargs)
            except Exception as err:
                logger.error(err, exc_info=True)
                raise
        return inner_wrapper

    return outer_wrapper


def init_logging():
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    logging.basicConfig(
        format=settings.LOG_FORMAT,
        datefmt=settings.LOG_DATE_FORMAT,
        level=logging.INFO
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
