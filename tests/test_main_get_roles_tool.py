"""Integration test for Redmine roles API via REST."""

import os
import sys
import pytest
import requests
from pprint import pprint

def test_main_get_roles_api():
    """Basic test for Redmine roles API via REST
    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    url = f"{REDMINE_URL.rstrip('/')}/roles.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    params = {}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "roles" in result
    assert isinstance(result["roles"], list)
    assert len(result["roles"]) > 0
    assert "id" in result["roles"][0]
    assert "name" in result["roles"][0]
