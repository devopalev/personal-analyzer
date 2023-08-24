import datetime

import pytest


@pytest.fixture()
def curr_datetime_utc():
    return datetime.datetime.now(tz=datetime.timezone.utc)
