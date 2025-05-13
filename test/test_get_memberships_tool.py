import os
from unittest.mock import MagicMock, patch

import pytest

from tools.get_memberships_tool import get_memberships


@pytest.fixture
def tool():
    return get_memberships


def mock_response(json_data, status=200):
    mock_resp = MagicMock()
    mock_resp.status_code = status
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status.side_effect = None if status == 200 else Exception("HTTP Error")
    return mock_resp


def test_run_success(tool):
    json_data = {
        "memberships": [{"id": 1, "user": {"id": 2, "name": "User"}}],
        "total_count": 1,
        "limit": 25,
        "offset": 0,
    }
    with patch("tools.get_memberships_tool.requests.get") as mock_get:
        mock_get.return_value = mock_response(json_data)
        result = tool("https://redmine.example.com", "dummykey", "testproject")
        assert result["memberships"] == json_data["memberships"]
        assert result["total_count"] == 1
        assert result["limit"] == 25
        assert result["offset"] == 0


def test_run_with_limit_offset(tool):
    json_data = {
        "memberships": [],
        "total_count": 0,
        "limit": 10,
        "offset": 5,
    }
    with patch("tools.get_memberships_tool.requests.get") as mock_get:
        mock_get.return_value = mock_response(json_data)
        result = tool("https://redmine.example.com", "dummykey", "testproject", limit=10, offset=5)
        assert result["limit"] == 10
        assert result["offset"] == 5


def test_run_http_error(tool):
    with patch("tools.get_memberships_tool.requests.get") as mock_get:
        mock_resp = mock_response({}, status=404)
        mock_resp.raise_for_status.side_effect = Exception("HTTP Error")
        mock_get.return_value = mock_resp
        with pytest.raises(Exception):
            tool("https://redmine.example.com", "dummykey", "testproject")


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
    assert "memberships" in result
    assert isinstance(result["memberships"], list)
