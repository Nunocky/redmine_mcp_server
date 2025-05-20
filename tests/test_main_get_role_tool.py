"""Integration test for Redmine role detail API via REST."""

import os
import sys
import pytest
import requests
from pprint import pprint


def test_main_get_role_api():
    """Basic test for Redmine role detail API via REST
    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    # まずロール一覧からIDを取得
    url = f"{REDMINE_URL.rstrip('/')}/roles.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    roles = data.get("roles", [])
    assert len(roles) > 0
    role_id = roles[0]["id"]

    # ロール詳細取得
    url_detail = f"{REDMINE_URL.rstrip('/')}/roles/{role_id}.json"
    response_detail = requests.get(url_detail, headers=headers)
    response_detail.raise_for_status()
    result = response_detail.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "role" in result
    role = result["role"]
    assert isinstance(role, dict)
    assert "id" in role
    assert "name" in role
    assert role["id"] == role_id
