import os
import sys
from pprint import pprint

import pytest
from dotenv import load_dotenv

from main import get_project

load_dotenv()


@pytest.mark.asyncio
async def test_get_project():
    """Normal case test for Redmine project details retrieval API

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL, REDMINE_ADMIN_API_KEY, and REDMINE_PROJECT_ID in .env.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    result = await get_project(redmine_url=redmine_url, api_key=api_key, project_id_or_identifier=project_id)
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result


@pytest.mark.asyncio
async def test_get_project_with_include():
    """Normal case test for Redmine project details retrieval API (with include specified)

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL, REDMINE_ADMIN_API_KEY, and REDMINE_PROJECT_ID in .env.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    result = await get_project(
        redmine_url=redmine_url, api_key=api_key, project_id_or_identifier=project_id, include="trackers,enabled_modules"
    )
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result
    # Check if the information specified by include is present
    if "trackers" in result:
        assert isinstance(result["trackers"], list)
    if "enabled_modules" in result:
        assert isinstance(result["enabled_modules"], list)
