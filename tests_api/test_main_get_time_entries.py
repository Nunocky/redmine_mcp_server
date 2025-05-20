import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_time_entries_basic():
    """Basic test for Redmine time_entries API via REST
    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    url = f"{REDMINE_URL.rstrip('/')}/time_entries.json"
    params = {"limit": 1}
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "time_entries" in result
