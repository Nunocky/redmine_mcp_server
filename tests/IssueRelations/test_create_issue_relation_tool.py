"""Issues API create_issue_relation 実機テスト

pytest -s tests/Issues/test_create_issue_relation_tool.py
"""

import os

from tools.IssueRelations.create_issue_relation import create_issue_relation


def test_create_issue_relation_success():
    """課題リレーション作成APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    # 事前に存在する課題IDを指定してください
    issue_id = os.environ.get("REDMINE_TEST_ISSUE_ID")
    issue_to_id = os.environ.get("REDMINE_TEST_ISSUE_TO_ID")
    relation_type = "relates"
    result = create_issue_relation(
        redmine_url=redmine_url,
        api_key=api_key,
        issue_id=int(issue_id),
        issue_to_id=int(issue_to_id),
        relation_type=relation_type,
    )
    print("result:", result)
    assert isinstance(result, dict)
    assert "relation" in result
    assert result["relation"]["issue_id"] == int(issue_id)
    assert result["relation"]["issue_to_id"] == int(issue_to_id)
    assert result["relation"]["relation_type"] == relation_type


def test_create_issue_relation_invalid_type():
    """不正なrelation_type指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    issue_id = os.environ.get("REDMINE_TEST_ISSUE_ID")
    issue_to_id = os.environ.get("REDMINE_TEST_ISSUE_TO_ID")
    result = create_issue_relation(
        redmine_url=redmine_url,
        api_key=api_key,
        issue_id=int(issue_id),
        issue_to_id=int(issue_to_id),
        relation_type="invalid_type",
    )
    print("result:", result)
    assert isinstance(result, dict)
    assert "error" in result or "message" in result or result == {}
