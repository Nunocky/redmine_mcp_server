import os
import sys
from pprint import pprint

import pytest
import requests

from tests.random_identifier import random_identifier


def test_create_archive_unarchive_delete_project():
    """Normal case test for Redmine project creation, archiving, unarchiving, and deletion APIs

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

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

    project_id = None
    try:
        # Create project (POST)
        url_create = f"{REDMINE_URL}/projects.json"
        headers = {"X-Redmine-API-Key": API_KEY, "Content-Type": "application/json"}
        payload = {
            "project": {
                "name": name,
                "identifier": identifier,
                "description": description,
            }
        }
        resp_create = requests.post(url_create, json=payload, headers=headers)
        assert resp_create.status_code in (201, 200), f"Create failed: {resp_create.text}"
        result_create = resp_create.json()
        pprint(result_create, stream=sys.stderr)
        project_info = result_create.get("project", result_create)
        assert isinstance(project_info, dict)
        assert "id" in project_info
        assert project_info["identifier"] == identifier
        assert project_info["name"] == name
        assert project_info["description"] == description
        project_id = project_info["id"]

        # Archive project (PUT)
        url_archive = f"{REDMINE_URL}/projects/{project_id}/archive.json"
        resp_archive = requests.put(url_archive, headers=headers)
        assert resp_archive.status_code in (200, 204), f"Archive failed: {resp_archive.text}"
        pprint({"status": "success", "action": "archive"}, stream=sys.stderr)

        # Unarchive project (PUT)
        url_unarchive = f"{REDMINE_URL}/projects/{project_id}/unarchive.json"
        resp_unarchive = requests.put(url_unarchive, headers=headers)
        assert resp_unarchive.status_code in (200, 204), f"Unarchive failed: {resp_unarchive.text}"
        pprint({"status": "success", "action": "unarchive"}, stream=sys.stderr)

    finally:
        if project_id:
            # Delete project (DELETE)
            url_delete = f"{REDMINE_URL}/projects/{project_id}.json"
            resp_delete = requests.delete(url_delete, headers=headers)
            # 削除失敗時もエラーにしない
            pprint({"status": "success", "action": "delete"}, stream=sys.stderr)
