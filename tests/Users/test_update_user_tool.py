import os
from pprint import pprint
import sys
import pytest

from tools.Users.update_user_tool import update_user

@pytest.fixture
def tool():
    return update_user

def test_update_user_success(tool):
    """
    Redmineの既存ユーザー情報を更新し、レスポンス内容を検証する。
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    user_id = os.getenv("REDMINE_TEST_USER_ID", "1")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(
        redmine_url,
        api_key,
        user_id=user_id,
        firstname="Updated",
        lastname="User"
    )
    pprint(result, stream=sys.stderr)
    # RedmineのPUT /users/:id.jsonは空レスポンスの場合もある
    assert isinstance(result, dict)

def test_update_user_not_found(tool):
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
            user_id=99999999,
            firstname="No",
            lastname="User"
        )
