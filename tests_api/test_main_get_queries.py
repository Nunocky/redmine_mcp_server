import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_queries():
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    url = f"{REDMINE_URL.rstrip('/')}/queries.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f"API request failed: {response.status_code} {response.text}"
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "queries" in result
    assert isinstance(result["queries"], list)
