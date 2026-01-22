import pytest
from test_data.builders.user_builder import UserBuilder


@pytest.fixture
def new_user():
    return UserBuilder().build()