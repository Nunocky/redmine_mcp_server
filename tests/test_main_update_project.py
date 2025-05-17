import os
import sys
from pprint import pprint

import pytest
from dotenv import load_dotenv

from main import create_project, delete_project, update_project
from tests.random_identifier import random_identifier

load_dotenv()


@pytest.mark.asyncio
async def test_create_update_delete_project():
    """Normal case test for Redmine project creation, update, and deletion APIs

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"

    identifier = random_identifier()
    name = "Test Project_" + identifier
    description = "Project for automated testing"

    # Create project
    result_create = await create_project(
        name=name, identifier=identifier, redmine_url=redmine_url, api_key=api_key, description=description
    )
    pprint(result_create, stream=sys.stderr)
    assert isinstance(result_create, dict)
    assert "id" in result_create
    assert result_create["identifier"] == identifier
    assert result_create["name"] == name
    assert result_create["description"] == description

    # Update project
    new_name = name + "_Updated"
    new_description = "Updated description"
    result_update = await update_project(
        project_id_or_identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
        name=new_name,
        description=new_description,
    )
    pprint(result_update, stream=sys.stderr)
    # According to Redmine's specification, an empty dict is returned for 204 No Content
    if result_update:
        assert isinstance(result_update, dict)
        if "name" in result_update:
            assert result_update["name"] == new_name
        if "description" in result_update:
            assert result_update["description"] == new_description

    # Delete project
    result_delete = await delete_project(project_id_or_identifier=identifier, redmine_url=redmine_url, api_key=api_key)
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "success"
