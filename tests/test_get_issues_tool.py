"""GetIssuesToolのテスト

GetIssuesToolを用いてRedmineの課題一覧取得APIの動作を検証する。
"""

import pytest
from tools.get_issues_tool import GetIssuesTool

@pytest.fixture
def tool():
    """GetIssuesToolのインスタンスを返す

    Returns:
        GetIssuesTool: テスト対象ツール
    """
    return GetIssuesTool()

def test_get_issues_basic(tool):
    """課題一覧が取得できることを検証する

    Args:
        tool (GetIssuesTool): テスト対象ツール
    """
    result = tool.run(limit=5)
    assert "issues" in result
    assert isinstance(result["issues"], list)
    assert len(result["issues"]) <= 5
    assert "total_count" in result
    assert "offset" in result
    assert "limit" in result

def test_get_issues_with_filters(tool):
    """フィルタ付きで課題一覧が取得できることを検証する

    Args:
        tool (GetIssuesTool): テスト対象ツール
    """
    filters = {"status_id": "open"}
    result = tool.run(limit=3, filters=filters)
    assert "issues" in result
    for issue in result["issues"]:
        # ステータス名が日本語の場合も考慮
        assert issue["status"]["name"] in ["New", "Open", "新規", "進行中"]
