import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_news():
    """Test get_news for all projects with real Redmine server."""
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    url = f"{REDMINE_URL}/news.json"
    params = {"limit": 5, "offset": 0}
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "news" in result
    assert isinstance(result["news"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result


def test_get_news_project():
    """Test get_news for a specific project with real Redmine server."""
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    PROJECT_ID = os.environ.get("REDMINE_TEST_PROJECT_ID")
    if not REDMINE_URL or not API_KEY or not PROJECT_ID:
        pytest.fail("REDMINE_URL, REDMINE_ADMIN_API_KEY, or REDMINE_TEST_PROJECT_ID is not set in .env")

    url = f"{REDMINE_URL}/projects/{PROJECT_ID}/news.json"
    params = {"limit": 5, "offset": 0}
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "news" in result
    assert isinstance(result["news"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result
