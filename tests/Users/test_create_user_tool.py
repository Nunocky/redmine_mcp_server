import os
import random
import string
import sys
from pprint import pprint

import pytest

from tools.Users.create_user import create_user


@pytest.fixture
def tool():
    return create_user


def random_login():
    return "testuser_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))


def test_create_user_success(tool):
    """
    Create a new user in Redmine and verify the response content.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    login = random_login()
    result = tool(
        redmine_url,
        api_key,
        login=login,
        firstname="Test",
        lastname="User",
        mail=f"{login}@example.com",
        password="password123",
    )
    pprint(result, stream=sys.stderr)
    assert "user" in result
    assert result["user"]["login"] == login


def test_create_user_missing_required(tool):
    """
    Verify that an error (Exception) occurs when required fields are missing.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, login="", firstname="", lastname="", mail="")
