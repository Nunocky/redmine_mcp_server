import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_issues():
    """Normal case test for Redmine issues list retrieval API

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
        Change project_id to an existing project identifier if needed.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    # You may need to change project_id to an existing one
    project_id = None  # None means all projects
    params = {}
    if project_id:
        params["project_id"] = project_id

    url = f"{REDMINE_URL}/issues.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    result_dict = response.json()
    pprint(result_dict, stream=sys.stderr)
    assert isinstance(result_dict, dict), "API response is not a dict type"
    assert "issues" in result_dict, "'issues' key does not exist in the response"
    assert isinstance(result_dict["issues"], list), "'issues' is not a list"
    # If there are no issues, the list may be empty, but the key must exist


def test_get_issues_notfound():
    """Test for non-existent project_id (should return empty issues list)

    Note:
        Redmine returns 404 for non-existent project_id.
        This test expects an empty issues list in that case.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    # Use a project_id that does not exist
    project_id = "project_id_that_does_not_exist_99999"
    params = {"project_id": project_id}

    url = f"{REDMINE_URL}/issues.json"
    headers = {"X-Redmine-API-Key": API_KEY}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 404:
        result_dict = {"issues": []}
    else:
        response.raise_for_status()
        result_dict = response.json()
    pprint(result_dict, stream=sys.stderr)
    assert isinstance(result_dict, dict), "API response is not a dict type"
    assert "issues" in result_dict, "'issues' key does not exist in the response"
    assert isinstance(result_dict["issues"], list), "'issues' is not a list"
    assert len(result_dict["issues"]) == 0, "Expected 'issues' to be empty for non-existent project"
