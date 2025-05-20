import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_memberships_tool():
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    PROJECT_ID = os.environ.get("REDMINE_TEST_PROJECT_ID")
    if not REDMINE_URL or not API_KEY or not PROJECT_ID:
        pytest.fail("REDMINE_URL, REDMINE_ADMIN_API_KEY, or REDMINE_TEST_PROJECT_ID is not set in .env")

    url = f"{REDMINE_URL}/projects/{PROJECT_ID}/memberships.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"API request failed: {response.status_code} {response.text}"
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "memberships" in result
    assert isinstance(result["memberships"], list)
