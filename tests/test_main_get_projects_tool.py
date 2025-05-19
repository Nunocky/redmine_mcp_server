import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_projects_tool():
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    url = f"{REDMINE_URL.rstrip('/')}/projects.json"
    params = {"limit": 5, "offset": 0}
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200, f"API request failed: {response.status_code} {response.text}"
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "projects" in result
    assert isinstance(result["projects"], list)
