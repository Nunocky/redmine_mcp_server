import os
import sys
from pprint import pprint

import pytest
import requests

from tests.random_identifier import random_identifier


def test_create_and_delete_project():
    """Normal case test for Redmine project creation and deletion APIs

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    REDMINE_URL = os.environ.get("REDMINE_URL")
    API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not REDMINE_URL or not API_KEY:
        pytest.fail("REDMINE_URL or REDMINE_ADMIN_API_KEY is not set in .env")
    identifier = random_identifier()
    name = "Test Project_" + identifier
    description = "Project for automated testing"
    headers = {"X-Redmine-API-Key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "project": {
            "name": name,
            "identifier": identifier,
            "description": description,
        }
    }
    response_create = requests.post(f"{REDMINE_URL}/projects.json", json=payload, headers=headers)
    result_create = response_create.json()
    pprint(result_create, stream=sys.stderr)
    assert response_create.status_code in (201, 200), f"Create failed: {response_create.text}"
    project_info = result_create.get("project", result_create)
    assert isinstance(project_info, dict)
    assert "id" in project_info
    assert project_info["identifier"] == identifier
    assert project_info["name"] == name
    assert project_info["description"] == description

    # プロジェクト削除
    response_delete = requests.delete(f"{REDMINE_URL}/projects/{identifier}.json", headers=headers)
    pprint(response_delete.text, stream=sys.stderr)
    assert response_delete.status_code in (200, 204), f"Delete failed: {response_delete.text}"
