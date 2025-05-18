import os
import sys
from pprint import pprint

import pytest

from main import archive_project, create_project, delete_project, unarchive_project
from tests.random_identifier import random_identifier


@pytest.mark.asyncio
async def test_create_archive_unarchive_delete_project():
    """Normal case test for Redmine project creation, archiving, unarchiving, and deletion APIs

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
        name=name,
        identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
        description=description,
    )
    pprint(result_create, stream=sys.stderr)
    assert isinstance(result_create, dict)
    assert "id" in result_create
    assert result_create["identifier"] == identifier
    assert result_create["name"] == name
    assert result_create["description"] == description

    # Archive project
    result_archive = await archive_project(
        project_id_or_identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
    )
    pprint(result_archive, stream=sys.stderr)
    assert result_archive["status"] == "success"

    # Unarchive project
    result_unarchive = await unarchive_project(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id_or_identifier=identifier,
    )
    pprint(result_unarchive, stream=sys.stderr)
    assert result_unarchive["status"] == "success"

    # Delete project
    result_delete = await delete_project(
        project_id_or_identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
    )
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "success"
