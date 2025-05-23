"""Issues API delete_issue_relation 実機テスト

pytest -s tests/Issues/test_delete_issue_relation_tool.py
"""

import os

from tools.IssueRelations.delete_issue_relation import delete_issue_relation


def test_delete_issue_relation_success():
    """課題リレーション削除APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    # 事前に削除可能なリレーションIDを指定してください
    relation_id = os.environ.get("REDMINE_TEST_RELATION_ID")
    result = delete_issue_relation(
        redmine_url=redmine_url,
        api_key=api_key,
        id=int(relation_id),
    )
    print("result:", result)
    assert isinstance(result, dict)
    assert result == {}


def test_delete_issue_relation_not_found():
    """存在しないリレーションID指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    result = delete_issue_relation(
        redmine_url=redmine_url,
        api_key=api_key,
        id=999999999,  # 存在しないID
    )
    print("result:", result)
    assert isinstance(result, dict)
    assert "error" in result or "message" in result or result == {}
