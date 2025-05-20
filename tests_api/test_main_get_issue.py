import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_issue():
    """Normal case test for Redmine issue retrieval API

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
        Change issue_id=1 to an existing issue ID.
    """
    issue_id = 1  # Please specify an existing issue ID
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    url = f"{REDMINE_URL}/issues/{issue_id}.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        result_dict = {"issue": None}
    else:
        response.raise_for_status()
        result_dict = response.json()
    pprint(result_dict, stream=sys.stderr)
    assert isinstance(result_dict, dict), "API response is not a dict type"
    assert "issue" in result_dict, "'issue' key does not exist in the response"
    assert result_dict["issue"] is not None, "Issue not found"
    assert result_dict["issue"]["id"] == issue_id, "Retrieved issue ID does not match"


def test_get_issue_notfound():
    """Test for non-existent issue_id (should return {'issue': None})"""
    issue_id = 999999  # unlikely to exist
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    url = f"{REDMINE_URL}/issues/{issue_id}.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        result_dict = {"issue": None}
    else:
        response.raise_for_status()
        result_dict = response.json()
    pprint(result_dict, stream=sys.stderr)
    assert isinstance(result_dict, dict), "API response is not a dict type"
    assert "issue" in result_dict, "'issue' key does not exist in the response"
    assert result_dict["issue"] is None, "Expected 'issue' to be None for non-existent ID"
