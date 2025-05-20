import os
import sys
from pprint import pprint

import pytest
import requests

from tests.random_identifier import random_identifier


def test_delete_project():
    """Normal case test for Redmine project deletion API"""
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")

    identifier = "deltest_" + random_identifier()
    name = "Project for deletion test_" + identifier
    description = "Project for deletion test"
    headers = {"X-Redmine-API-Key": API_KEY, "Content-Type": "application/json"}
    payload = {"project": {"name": name, "identifier": identifier, "description": description}}
    resp_create = requests.post(f"{REDMINE_URL}/projects.json", json=payload, headers=headers)
    result_create = resp_create.json()
    pprint(result_create, stream=sys.stderr)
    assert resp_create.status_code in (201, 200), f"Create failed: {resp_create.text}"
    project_info = result_create.get("project", result_create)
    assert isinstance(project_info, dict)
    assert "identifier" in project_info and project_info["identifier"] == identifier

    # プロジェクト削除
    resp_delete = requests.delete(f"{REDMINE_URL}/projects/{identifier}.json", headers=headers)
    pprint({"status_code": resp_delete.status_code, "text": resp_delete.text}, stream=sys.stderr)
    assert resp_delete.status_code in (200, 204), f"Delete failed: {resp_delete.text}"


def test_delete_nonexistent_project():
    """Test for deleting a non-existent Redmine project API"""
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")
    nonexistent_id = "nonexistent_project_" + random_identifier()
    resp_delete = requests.delete(f"{REDMINE_URL}/projects/{nonexistent_id}.json", headers={"X-Redmine-API-Key": API_KEY})
    pprint({"status_code": resp_delete.status_code, "text": resp_delete.text}, stream=sys.stderr)
    assert resp_delete.status_code == 404
