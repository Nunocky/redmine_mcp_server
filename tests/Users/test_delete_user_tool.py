import os
import sys
from pprint import pprint

import pytest

from tools.Users.delete_user_tool import delete_user


@pytest.fixture
def tool():
    return delete_user


def test_delete_user_success(tool):
    """
    Delete an existing user in Redmine and verify the response content.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_DELETE_USER_ID")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    if not user_id:
        pytest.skip("Skipping because REDMINE_TEST_DELETE_USER_ID is not set")
    result = tool(redmine_url, api_key, user_id=int(user_id))
    pprint(result, stream=sys.stderr)
    assert result["deleted"] is True


def test_delete_user_not_found(tool):
    """
    Verify that an HTTP error (Exception) occurs when requesting with a non-existent user ID.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, user_id=99999999)
