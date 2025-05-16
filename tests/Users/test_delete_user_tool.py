import os
from pprint import pprint
import sys
import pytest

from tools.Users.delete_user_tool import delete_user

@pytest.fixture
def tool():
    return delete_user

def test_delete_user_success(tool):
    """
    Redmineの既存ユーザーを削除し、レスポンス内容を検証する。
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_DELETE_USER_ID")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    if not user_id:
        pytest.skip("REDMINE_TEST_DELETE_USER_IDが未設定のためスキップ")
    result = tool(
        redmine_url,
        api_key,
        user_id=int(user_id)
    )
    pprint(result, stream=sys.stderr)
    assert result["deleted"] is True

def test_delete_user_not_found(tool):
    """
    存在しないユーザーIDでリクエストし、HTTPエラー(Exception)が発生することを検証する。
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(
            redmine_url,
            api_key,
            user_id=99999999
        )
