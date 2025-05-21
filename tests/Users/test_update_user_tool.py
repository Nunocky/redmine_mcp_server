import os
import sys
from pprint import pprint

import pytest

from tools.Users.update_user import update_user


@pytest.fixture
def tool():
    return update_user


def test_update_user_success(tool):
    """
    Update existing user information in Redmine and verify the response content.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_USER_ID", "1")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, user_id=user_id, firstname="Updated", lastname="User")
    pprint(result, stream=sys.stderr)
    # Redmine's PUT /users/:id.json may return an empty response
    assert isinstance(result, dict)


def test_update_user_not_found(tool):
    """
    Verify that an HTTP error (Exception) occurs when requesting with a non-existent user ID.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, user_id=99999999, firstname="No", lastname="User")
