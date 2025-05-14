import os
from pprint import pprint
import sys
import pytest

from tools.get_memberships_tool import get_memberships


@pytest.fixture
def tool():
    return get_memberships


def test_run_success(tool):
    """
    実際のRedmineサーバーにアクセスして memberships を取得し、基本的な項目を検証する。
    """
    api_key = os.getenv("REDMINE_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, "testproject")
    pprint(result, stream=sys.stderr)
    assert "memberships" in result
    assert isinstance(result["memberships"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result


def test_run_with_limit_offset(tool):
    """
    実際のRedmineサーバーにアクセスし、limit/offset指定で memberships を取得して検証する。
    """
    api_key = os.getenv("REDMINE_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = tool(redmine_url, api_key, "testproject", limit=10, offset=5)
    pprint(result, stream=sys.stderr)
    assert result["limit"] == 10
    assert result["offset"] == 5


def test_run_http_error(tool):
    """
    存在しないプロジェクトIDでリクエストし、HTTPエラー(Exception)が発生することを検証する。
    """
    api_key = os.getenv("REDMINE_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    with pytest.raises(Exception):
        tool(redmine_url, api_key, "nonexistent_project_404")


def test_run_real_redmine():
    """
    実際のRedmineサーバー(.envのREDMINE_URL)にアクセスして memberships を取得する統合テスト。
    既知のAPIキーを使い、testproject から memberships を取得します。
    """
    api_key = os.getenv("REDMINE_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    result = get_memberships(redmine_url, api_key, "testproject")
    pprint(result, stream=sys.stderr)
    assert "memberships" in result
    assert isinstance(result["memberships"], list)
