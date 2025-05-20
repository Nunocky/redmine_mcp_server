import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_project():
    """Normal case test for Redmine project details retrieval API
    Note:
        Please set REDMINE_URL, REDMINE_ADMIN_API_KEY, and REDMINE_PROJECT_ID in .env.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    PROJECT_ID = os.environ.get("REDMINE_TEST_PROJECT_ID")
    if not REDMINE_URL or not API_KEY or not PROJECT_ID:
        pytest.fail("REDMINE_URL, REDMINE_ADMIN_API_KEY, or REDMINE_TEST_PROJECT_ID is not set in .env")

    url = f"{REDMINE_URL}/projects/{PROJECT_ID}.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    result = response.json().get("project", response.json())
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result


def test_get_project_with_include():
    """Normal case test for Redmine project details retrieval API (with include specified)
    Note:
        Please set REDMINE_URL, REDMINE_ADMIN_API_KEY, and REDMINE_PROJECT_ID in .env.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    PROJECT_ID = os.environ.get("REDMINE_TEST_PROJECT_ID")
    if not REDMINE_URL or not API_KEY or not PROJECT_ID:
        pytest.fail("REDMINE_URL, REDMINE_ADMIN_API_KEY, or REDMINE_TEST_PROJECT_ID is not set in .env")

    url = f"{REDMINE_URL}/projects/{PROJECT_ID}.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    params = {"include": "trackers,enabled_modules"}
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    result = response.json().get("project", response.json())
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result
    if "trackers" in result:
        assert isinstance(result["trackers"], list)
    if "enabled_modules" in result:
        assert isinstance(result["enabled_modules"], list)
