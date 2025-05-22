"""News APIの実機テスト

pytest -s tests/News/test_get_news.py
"""

import os

import pytest

from tools.News.get_news import get_news


def test_get_news_all_projects():
    """全プロジェクトのニュース取得APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")  # or os.environ.get("REDMINE_ADMIN_API_KEY")
    result = get_news(
        redmine_url=redmine_url,
        api_key=api_key,
    )
    print("result:", result)
    assert "news" in result
    assert "total_count" in result
    assert isinstance(result["news"], list)


def test_get_news_with_project():
    """特定プロジェクトのニュース取得APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")  # or os.environ.get("REDMINE_ADMIN_API_KEY")
    # プロジェクトIDは事前に存在するものを指定してください
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    result = get_news(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
    )
    print("result:", result)
    assert "news" in result
    assert "total_count" in result
    assert isinstance(result["news"], list)


def test_get_news_invalid_project():
    """存在しないプロジェクトID指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")  # or os.environ.get("REDMINE_ADMIN_API_KEY")
    with pytest.raises(ValueError):
        get_news(
            redmine_url=redmine_url,
            api_key=api_key,
            project_id="__not_exist_project__",
        )
