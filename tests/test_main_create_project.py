import os
import sys
from pprint import pprint

import pytest

from main import create_project, delete_project
from tests.random_identifier import random_identifier

REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")


def test_create_and_delete_project():
    """Normal case test for Redmine project creation and deletion APIs

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    identifier = random_identifier()
    name = "Test Project_" + identifier
    description = "Project for automated testing"

    # Create project
    result_create = create_project(
        name=name,
        identifier=identifier,
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
        description=description,
    )
    if hasattr(result_create, "__await__"):
        import asyncio

        result_create = asyncio.run(result_create)
    pprint(result_create, stream=sys.stderr)
    # 柔軟にproject情報を取得
    if "id" in result_create:
        project_info = result_create
    elif "project" in result_create and isinstance(result_create["project"], dict):
        project_info = result_create["project"]
    else:
        project_info = {}
    assert isinstance(project_info, dict)
    assert "id" in project_info
    assert project_info["identifier"] == identifier
    assert project_info["name"] == name
    assert project_info["description"] == description

    # Delete project
    result_delete = delete_project(
        project_id_or_identifier=identifier,
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
    )
    if hasattr(result_delete, "__await__"):
        import asyncio

        result_delete = asyncio.run(result_delete)
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "success"
