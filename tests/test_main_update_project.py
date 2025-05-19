import logging
import os

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

import pytest
import requests

from tests.random_identifier import random_identifier


def test_create_update_delete_project():
    """Normal case test for Redmine project creation, update, and deletion APIs (requests library version)

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

    # Create project
    create_url = f"{REDMINE_URL}/projects.json"
    headers = {"X-Redmine-API-Key": API_KEY, "Content-Type": "application/json"}
    payload = {"project": {"name": name, "identifier": identifier, "description": description}}
    resp_create = requests.post(create_url, json=payload, headers=headers)
    try:
        result_create = resp_create.json()
        assert resp_create.status_code in (201, 200), (
            f"Create failed with status code {resp_create.status_code}: {resp_create.text}"
        )
    except requests.exceptions.JSONDecodeError as e:
        pytest.fail(f"Failed to decode JSON response: {e}")

    assert resp_create.status_code in (201, 200), f"Create failed: {resp_create.text}"
    project_info = result_create.get("project", result_create)
    assert project_info["identifier"] == identifier
    assert project_info["name"] == name
    new_name = f"{name}_Updated"
    new_description = "Updated description"

    # Update project
    new_name = name + "_Updated"
    new_description = "Updated description"
    update_url = f"{REDMINE_URL}/projects/{identifier}.json"
    update_payload = {"project": {"name": new_name, "description": new_description}}
    resp_update = requests.put(update_url, json=update_payload, headers=headers)
    assert resp_update.status_code in (200, 204), f"Update failed: {resp_update.text}"
    if resp_update.status_code == 200:
        try:
            result_update = resp_update.json()
            if "project" in result_update:
                result_update = result_update["project"]
            else:
                pytest.fail(f"Response JSON does not contain 'project' key: {result_update}")
            logging.debug(f"Update response: {result_update}")
            assert result_update["name"] == new_name
            assert result_update["description"] == new_description
        except requests.exceptions.JSONDecodeError as e:
            pytest.fail(f"Failed to decode JSON response during update: {e}")
    else:
        logging.debug(f"Update status code: {resp_update.status_code}")

    # Delete project
    delete_url = f"{REDMINE_URL}/projects/{identifier}.json"
    resp_delete = requests.delete(delete_url, headers=headers)
    logging.debug({"status_code": resp_delete.status_code})
    logging.debug(f"Delete status code: {resp_delete.status_code}")
    try:
        result_delete = resp_delete.json()
        logging.debug(f"Delete response: {result_delete}")
    except requests.exceptions.JSONDecodeError:
        result_delete = None
        logging.error("No valid JSON response received during delete")
    assert resp_delete.status_code in (200, 204), f"Delete failed: {resp_delete.text}"
