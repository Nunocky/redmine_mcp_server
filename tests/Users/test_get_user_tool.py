import os
import sys
from pprint import pprint

import pytest

from tools.Users.get_user import get_user


@pytest.fixture
def tool():
    return get_user


def test_run_success(tool):
    """
    Access the actual Redmine server to retrieve user information and verify basic items.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_USER_ID", "1")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, user_id)
    pprint(result, stream=sys.stderr)
    assert "user" in result
    assert "id" in result["user"]
    assert "login" in result["user"]


def test_run_http_error(tool):
    """
    Verify that an HTTP error (Exception) occurs when requesting with a non-existent user ID.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, 99999999)


def test_run_with_current_user(tool):
    """
    Use the /users/current endpoint to retrieve user information and verify basic items.
    """
    api_key = os.getenv("REDMINE_USER_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_USER_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, "current")
    pprint(result, stream=sys.stderr)
    assert "user" in result
    assert "id" in result["user"]
    assert "login" in result["user"]
    assert "api_key" in result["user"]  # User's own information includes api_key


def test_run_with_include_memberships(tool):
    """
    Use the include=memberships parameter to retrieve user information and verify that membership information is included.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_USER_ID", "1")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, user_id, include="memberships")
    pprint(result, stream=sys.stderr)
    assert "user" in result
    assert "memberships" in result["user"]


def test_run_with_include_groups(tool):
    """
    Use the include=groups parameter to retrieve user information and verify that group information is included.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_USER_ID", "1")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, user_id, include="groups")
    pprint(result, stream=sys.stderr)
    assert "user" in result
    assert "groups" in result["user"]


def test_run_with_include_memberships_and_groups(tool):
    """
    Use the include=memberships,groups parameter to retrieve user information and
    verify that both membership and group information are included.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_USER_ID", "1")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, user_id, include="memberships,groups")
    pprint(result, stream=sys.stderr)
    assert "user" in result
    assert "memberships" in result["user"]
    assert "groups" in result["user"]


def test_run_locked_user_returns_404(tool):
    """
    Verify that a 404 error (Exception) occurs when specifying a locked user ID.
    """
    api_key = os.getenv("REDMINE_LOCKED_USER_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_LOCKED_USER_ID")
    assert api_key, "REDMINE_LOCKED_USER_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert user_id, "REDMINE_LOCKED_USER_ID is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, user_id)
