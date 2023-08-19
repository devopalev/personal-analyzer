import logging
from functools import wraps
from typing import Callable

from telegram import Update


def logger(logger_name: str):
    def outer_wrapper(function: Callable) -> Callable:
        @wraps(function)
        async def inner_wrapper(*args, **kwargs) -> Callable:
            logger = logging.getLogger(logger_name)

            if args and isinstance(args[0], Update):
                update = args[0]
                username = update.effective_user.username
                user_id = update.effective_user.id
                logger.info(f"{username}({user_id}): {update}")
            else:
                logger.info(args, kwargs)
            return await function(*args, **kwargs)

        return inner_wrapper

    return outer_wrapper
