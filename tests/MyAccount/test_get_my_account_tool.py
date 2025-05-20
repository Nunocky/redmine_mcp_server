"""Test for get_my_account function in get_my_account_tool.py."""

import os

import pytest

from tools.MyAccount.get_my_account_tool import get_my_account


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        pytest.fail(f"環境変数 {key} が未設定のため終了")
    return value


def test_get_my_account_json():
    base_url = get_env("REDMINE_URL")
    api_key = get_env("REDMINE_USER_API_KEY")

    user = get_my_account(
        base_url=base_url,
        api_key=api_key,
    )
    print(user)
    # Check required fields
    assert isinstance(user, dict)
    assert "user" in user
    user_info = user["user"]
    assert "id" in user_info
    assert "login" in user_info
    assert "firstname" in user_info
    assert "lastname" in user_info
    assert "mail" in user_info


def test_get_my_account_invalid_key():
    """Test get_my_account raises Exception with invalid API key."""
    base_url = get_env("REDMINE_URL")
    with pytest.raises(Exception):
        get_my_account(
            base_url=base_url,
            api_key="invalid_key",
        )
