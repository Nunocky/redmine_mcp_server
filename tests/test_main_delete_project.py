import os
import random
import string
import sys
from pprint import pprint

import pytest
from dotenv import load_dotenv

from main import create_project, delete_project
from tests.random_identifier import random_identifier

load_dotenv()


@pytest.mark.asyncio
async def test_delete_project():
    """Normal case test for Redmine project deletion API

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
    name = "Project for deletion test_" + identifier

    # Create project
    result_create = await create_project(
        name=name, identifier=identifier, redmine_url=redmine_url, api_key=api_key, description="Project for deletion test"
    )
    pprint(result_create, stream=sys.stderr)
    assert isinstance(result_create, dict)
    assert "id" in result_create
    assert result_create["identifier"] == identifier

    # Delete project
    result_delete = await delete_project(project_id_or_identifier=identifier, redmine_url=redmine_url, api_key=api_key)
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "success"


@pytest.mark.asyncio
async def test_delete_nonexistent_project():
    """Test for deleting a non-existent Redmine project API

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

    # Specify a non-existent project ID
    nonexistent_id = "nonexistent_project_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # Delete project
    result_delete = await delete_project(project_id_or_identifier=nonexistent_id, redmine_url=redmine_url, api_key=api_key)
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "error"
    assert "status_code" in result_delete
