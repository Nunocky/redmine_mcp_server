import os
import sys
from pprint import pprint

import pytest

from tools.News.get_news_tool import get_news


def test_get_news():
    """Test get_news for all projects with real Redmine server.

    This test requires the following environment variables:
        - REDMINE_URL
        - REDMINE_ADMIN_API_KEY
        - REDMINE_TEST_PROJECT_ID

    The test will fetch news for all projects and check the response structure.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    # Fetch news for all projects (project_id is not used for all-projects)
    result = get_news(
        redmine_url=redmine_url,
        api_key=api_key,
        limit=5,
        offset=0,
    )
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "news" in result
    assert isinstance(result["news"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result


def test_get_news_invalid_project():
    """存在しないプロジェクトID指定時のエラー系テスト（実API呼び出し）"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    # 存在しないプロジェクトIDを明示的に指定
    invalid_project_id = "__not_exist_project__"
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    with pytest.raises(ValueError):
        get_news(
            redmine_url=redmine_url,
            api_key=api_key,
            project_id=invalid_project_id,
            limit=1,
            offset=0,
        )


def test_get_news_project():
    """Test get_news for a specific project with real Redmine server.

    This test requires the following environment variables:
        - REDMINE_URL
        - REDMINE_ADMIN_API_KEY
        - REDMINE_TEST_PROJECT_ID

    The test will fetch news for the specified project and check the response structure.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    # Fetch news for the specified project
    result = get_news(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
        limit=5,
        offset=0,
    )
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "news" in result
    assert isinstance(result["news"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result
