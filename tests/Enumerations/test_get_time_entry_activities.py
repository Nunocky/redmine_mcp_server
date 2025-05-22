"""TimeEntryActivities APIの実機テスト

pytest -s tests/Enumerations/test_get_time_entry_activities.py
"""

import os

import pytest

from tools.Enumerations.get_time_entry_activities import get_time_entry_activities


def test_get_time_entry_activities_normal():
    """タイムエントリー活動一覧取得APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    result = get_time_entry_activities(redmine_url=redmine_url, api_key=api_key)
    print("result:", result)
    assert "time_entry_activities" in result
    assert isinstance(result["time_entry_activities"], list)


def test_get_time_entry_activities_invalid_url():
    """不正なURL指定時のエラー系テスト"""
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    with pytest.raises(Exception):
        get_time_entry_activities(redmine_url="http://invalid-url", api_key=api_key)


def test_get_time_entry_activities_invalid_key():
    """不正なAPIキー指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    result = get_time_entry_activities(redmine_url=redmine_url, api_key="invalid_key")
    # APIキーが不正な場合、Redmineは403や空リストを返す場合がある
    assert "time_entry_activities" not in result or not result["time_entry_activities"]
