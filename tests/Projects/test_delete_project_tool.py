import os
import pprint
import random
import string

import pytest

from tests.random_identifier import random_identifier
from tools.Projects.create_project_tool import create_project
from tools.Projects.delete_project_tool import delete_project


def test_delete_project_real_api():
    """Real API: Test for project deletion"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("Skipping because REDMINE_URL and REDMINE_ADMIN_API_KEY are not set")

    identifier = random_identifier()
    name = "Test Deletion Project_" + identifier

    # Create project
    result_create = create_project(
        name=name, identifier=identifier, redmine_url=redmine_url, api_key=api_key, description="Project for deletion test"
    )
    pprint.pprint(result_create)
    assert "id" in result_create
    assert result_create["identifier"] == identifier

    # Delete project
    result_delete = delete_project(identifier, redmine_url=redmine_url, api_key=api_key)
    pprint.pprint(result_delete)
    assert result_delete["status"] == "success"
    assert result_delete["message"] == "Project deleted"


def test_delete_nonexistent_project_real_api():
    """Real API: Test for deleting a non-existent project"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("Skipping because REDMINE_URL and REDMINE_ADMIN_API_KEY are not set")

    # Specify a non-existent project ID
    nonexistent_id = "nonexistent_project_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # Delete project
    result_delete = delete_project(nonexistent_id, redmine_url=redmine_url, api_key=api_key)
    pprint.pprint(result_delete)
    assert result_delete["status"] == "error"
    assert "status_code" in result_delete
