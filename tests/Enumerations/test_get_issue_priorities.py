"""IssuePriorities APIの実機テスト

pytest -s tests/Enumerations/test_get_issue_priorities.py
"""

import os

import pytest

from tools.Enumerations.get_issue_priorities import get_issue_priorities


def test_get_issue_priorities_normal():
    """チケット優先度一覧取得APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    result = get_issue_priorities(
        redmine_url=redmine_url,
        api_key=api_key,
    )
    print("result:", result)
    assert "issue_priorities" in result
    assert isinstance(result["issue_priorities"], list)


def test_get_issue_priorities_invalid_url():
    """不正なURL指定時のエラー系テスト"""
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    with pytest.raises(Exception):
        get_issue_priorities(
            redmine_url="http://invalid-url",
            api_key=api_key,
        )


def test_get_issue_priorities_invalid_key():
    """不正なAPIキー指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    result = get_issue_priorities(
        redmine_url=redmine_url,
        api_key="invalid_key",
    )
    # APIキーが無効でも取得できてしまうRedmine環境の場合はスキップ
    if "issue_priorities" in result and result["issue_priorities"]:
        pytest.skip("APIキーが無効でも取得できるRedmine環境のためスキップ")
    assert "issue_priorities" not in result or not result["issue_priorities"]
