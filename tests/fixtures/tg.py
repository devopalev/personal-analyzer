import pytest
from telegram import Chat
from telegram import User
from telegram.constants import ChatType
from telegram.ext import CallbackContext


async def fake_send_message(self, text="", **kwargs):
    self.test_storage["text"] = text
    return True


@pytest.fixture()
def user_test():
    # monkey pathing
    User.send_message = fake_send_message
    User.test_storage = {}

    user = User(
        first_name="test_first_name",
        id=123456789,
        is_bot=False,
        is_premium=True,
        language_code="ru",
        last_name="test_last_name",
        username="test_username",
    )
    return user


@pytest.fixture()
def chat_private(user_test):
    return Chat(
        first_name=user_test.first_name,
        id=user_test.id,
        last_name=user_test.last_name,
        type=ChatType.PRIVATE,
        username=user_test.username,
    )


@pytest.fixture()
def chat_channel():
    return Chat(id=-1000000000001, title="Personal Channel", type=ChatType.CHANNEL)


@pytest.fixture()
def user_bot_test():
    return User(
        first_name="Personal Bot Analyzer",
        id=111222333,
        is_bot=True,
        username="personal_analyzer_bot",
    )


@pytest.fixture()
def context():
    test_storage = {}

    class Bot:
        async def send_message(self, tg_id, *args, text="", **kwargs):
            test_storage["text"] = text

    CallbackContext.test_storage = test_storage
    CallbackContext.bot = Bot()
    return CallbackContext(None)
