"""GetIssuesToolのテスト

GetIssuesToolを用いてRedmineの課題一覧取得APIの動作を検証する。
"""

from tools.Issues.get_issues_tool import get_issues

def test_get_issues_basic():
    """課題一覧が取得できることを検証する

    Returns:
        None
    """
    result = get_issues(limit=5)
    assert "issues" in result
    assert isinstance(result["issues"], list)
    assert len(result["issues"]) <= 5
    assert "total_count" in result
    assert "offset" in result
    assert "limit" in result

def test_get_issues_with_filters():
    """フィルタ付きで課題一覧が取得できることを検証する

    Returns:
        None
    """
    filters = {"status_id": "open"}
    result = get_issues(limit=3, filters=filters)
    assert "issues" in result
    for issue in result["issues"]:
        # ステータス名が日本語の場合も考慮
        assert issue["status"]["name"] in ["New", "Open", "新規", "進行中"]

def test_get_issues_with_offset_and_limit():
    """offsetとlimitでページングできることを検証する"""
    result = get_issues(offset=2, limit=2)
    assert "issues" in result
    assert len(result["issues"]) <= 2
    assert result["offset"] == 2

def test_get_issues_with_sort():
    """sortパラメータでソートできることを検証する"""
    result = get_issues(sort="updated_on:desc", limit=3)
    dates = [issue["updated_on"] for issue in result["issues"]]
    assert dates == sorted(dates, reverse=True)

def test_get_issues_with_include():
    """includeパラメータでattachments等が取得できることを検証する"""
    result = get_issues(include="attachments", limit=1)
    assert "issues" in result
    for issue in result["issues"]:
        assert "attachments" in issue

def test_get_issues_with_multiple_filters():
    """複数フィルタで絞り込みできることを検証する"""
    filters = {"project_id": 1, "tracker_id": 2}
    result = get_issues(filters=filters, limit=2)
    for issue in result["issues"]:
        assert issue["project"]["id"] == 1
        assert issue["tracker"]["id"] == 2

def test_get_issues_with_invalid_filter():
    """存在しないproject_idなどで0件になることを検証する"""
    filters = {"project_id": 999999}
    result = get_issues(filters=filters)
    assert result["total_count"] == 0

def test_get_issues_api_error(monkeypatch):
    """APIエラー時に例外が発生することを検証する"""
    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 404

            def raise_for_status(self):
                from requests.exceptions import HTTPError
                raise HTTPError(f"404 Client Error: Not Found for url: {kwargs.get('url', '')}")
        return MockResponse()
    monkeypatch.setattr("tools.redmine_api_client.RedmineAPIClient.get", mock_get)
    try:
        get_issues()
        assert False, "Exception not raised"
    except Exception:
        assert True
