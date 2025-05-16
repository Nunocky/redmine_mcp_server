import os
from pprint import pprint
import sys
import pytest

from tools.Users.get_user_tool import get_user

@pytest.fixture
def tool():
    return get_user

def test_run_success(tool):
    """
    実際のRedmineサーバーにアクセスしてユーザー情報を取得し、基本的な項目を検証する。
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
    存在しないユーザーIDでリクエストし、HTTPエラー(Exception)が発生することを検証する。
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, 99999999)

def test_run_with_current_user(tool):
    """
    /users/current エンドポイントを使用してユーザー情報を取得し、基本的な項目を検証する。
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
    assert "api_key" in result["user"]  # 自分自身のユーザー情報にはapi_keyが含まれる

def test_run_with_include_memberships(tool):
    """
    include=memberships パラメータを使用してユーザー情報を取得し、メンバーシップ情報が含まれることを検証する。
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
    include=groups パラメータを使用してユーザー情報を取得し、グループ情報が含まれることを検証する。
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
    include=memberships,groups パラメータを使用してユーザー情報を取得し、
    メンバーシップ情報とグループ情報の両方が含まれることを検証する。
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
    ロックされたユーザーIDを指定した場合に404エラー(Exception)となることを検証する。
    """
    api_key = os.getenv("REDMINE_LOCKED_USER_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_LOCKED_USER_ID")
    assert api_key, "REDMINE_LOCKED_USER_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert user_id, "REDMINE_LOCKED_USER_ID is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, user_id)
