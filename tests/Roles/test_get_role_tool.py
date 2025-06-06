"""Test for get_role (Redmine Roles API)."""

import os

import pytest

from tools.Roles.get_role import get_role
from tools.Roles.get_roles import get_roles


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        pytest.fail(f"環境変数 {key} が未設定")
    return value


def test_get_role():
    """Redmineロール詳細取得APIの正常系テスト"""
    redmine_url = get_env("REDMINE_URL")
    api_key = get_env("REDMINE_USER_API_KEY")
    roles_result = get_roles(
        redmine_url=redmine_url,
        api_key=api_key,
    )
    roles = roles_result["roles"]
    assert len(roles) > 0
    role_id = roles[0]["id"]

    result = get_role(
        redmine_url=redmine_url,
        api_key=api_key,
        role_id=role_id,
    )
    print("result:", result)
    assert "role" in result
    role = result["role"]
    assert isinstance(role, dict)
    assert "id" in role
    assert "name" in role
    assert role["id"] == role_id
