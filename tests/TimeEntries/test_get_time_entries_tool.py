"""Tests for GetTimeEntriesTool."""

import os

from tools.TimeEntries.get_time_entries_tool import get_time_entries


def test_get_time_entries_success():
    """Test successful retrieval of time entries using real Redmine API."""
    # 環境変数から必要な情報を取得
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    project_id = os.getenv("REDMINE_TEST_PROJECT_ID")

    # 環境変数が設定されていることを確認
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    # 実際のAPIを呼び出す
    result = get_time_entries(
        redmine_url=redmine_url,
        api_key=api_key,
        limit=5,
        project_id=project_id,
    )

    # レスポンスの検証
    assert "time_entries" in result
    assert "total_count" in result
    assert isinstance(result["time_entries"], list)


def test_get_time_entries_with_filters():
    """Test time entries retrieval with various filters."""
    # 環境変数から必要な情報を取得
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")

    # 環境変数が設定されていることを確認
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"

    # 実際のAPIを呼び出す（フィルター付き）
    result = get_time_entries(
        redmine_url=redmine_url,
        api_key=api_key,
        limit=3,
        from_date="2025-01-01",
        to_date="2025-12-31",
    )

    # レスポンスの検証
    assert "time_entries" in result
    assert "total_count" in result
