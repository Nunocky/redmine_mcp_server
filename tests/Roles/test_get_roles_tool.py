"""Test for get_roles (Redmine Roles API)."""

import os
import pytest
from tools.Roles.get_roles_tool import get_roles


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        pytest.fail(f"環境変数 {key} が未設定")
    return value


def test_get_roles():
    """Redmineロール一覧取得APIの正常系テスト"""
    redmine_url = get_env("REDMINE_URL")
    api_key = get_env("REDMINE_USER_API_KEY")
    result = get_roles(
        redmine_url=redmine_url,
        api_key=api_key,
    )
    print("result:", result)
    assert "roles" in result
    assert isinstance(result["roles"], list)
    assert len(result["roles"]) > 0
    assert "id" in result["roles"][0]
    assert "name" in result["roles"][0]
