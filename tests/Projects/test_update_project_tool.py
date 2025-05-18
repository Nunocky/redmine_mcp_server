import os
import pprint

import pytest

from tests.random_identifier import random_identifier
from tools.Projects.create_project_tool import create_project
from tools.Projects.delete_project_tool import delete_project
from tools.Projects.update_project_tool import update_project


def test_create_update_delete_project_real_api():
    """Real API: Create project -> Update -> Delete"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("Skipping because REDMINE_URL and REDMINE_ADMIN_API_KEY are not set")

    identifier = random_identifier()
    name = "Test Project_" + identifier

    # Create project
    result_create = create_project(
        name=name, identifier=identifier, redmine_url=redmine_url, api_key=api_key, description="Project for automated testing"
    )
    pprint.pprint(result_create)
    assert "id" in result_create
    assert result_create["identifier"] == identifier

    # Update project
    new_name = name + "_Updated"
    new_description = "Updated description"
    result_update = update_project(
        identifier, redmine_url=redmine_url, api_key=api_key, name=new_name, description=new_description
    )
    pprint.pprint(result_update)
    # According to Redmine's specification, an empty dict is returned for 204 No Content
    if result_update:
        assert "id" in result_update
        assert result_update["name"] == new_name
        assert result_update["description"] == new_description
    else:
        # If it's an empty dict, consider the update successful
        assert result_update == {}

    # Delete project
    result_delete = delete_project(identifier, redmine_url=redmine_url, api_key=api_key)
    pprint.pprint(result_delete)
    assert result_delete["status"] == "success"
