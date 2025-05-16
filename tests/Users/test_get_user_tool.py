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
    api_key = os.getenv("REDMINE_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_USER_ID", "1")
    assert api_key, "REDMINE_API_KEY is not set in .env"
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
    api_key = os.getenv("REDMINE_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, 99999999)
