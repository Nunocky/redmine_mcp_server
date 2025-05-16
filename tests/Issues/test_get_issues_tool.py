"""GetIssuesToolのテスト

GetIssuesToolを用いてRedmineの課題一覧取得APIの動作を検証する。
"""

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
