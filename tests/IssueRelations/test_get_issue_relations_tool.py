"""Issues API get_issue_relations 実機テスト

pytest -s tests/Issues/test_get_issue_relations_tool.py
"""

import os

from tools.IssueRelations.get_issue_relations import get_issue_relations


def test_get_issue_relations_success():
    """課題リレーション一覧取得APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    # 事前にリレーションが存在する課題IDを指定してください
    issue_id = os.environ.get("REDMINE_TEST_ISSUE_ID")
    result = get_issue_relations(
        redmine_url=redmine_url,
        api_key=api_key,
        issue_id=int(issue_id),
    )
    print("result:", result)
    assert isinstance(result, dict)
    assert "relations" in result


def test_get_issue_relations_not_found():
    """存在しない課題ID指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    result = get_issue_relations(
        redmine_url=redmine_url,
        api_key=api_key,
        issue_id=999999999,  # 存在しないID
    )
    print("result:", result)
    # 仕様によりエラー内容はAPIクライアント依存
    assert isinstance(result, dict)
    assert "error" in result or "message" in result or result == {}
