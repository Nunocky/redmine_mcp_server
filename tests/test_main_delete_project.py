import os
import random
import string
import sys
from pprint import pprint

from tests.random_identifier import random_identifier
from tools.Projects.create_project_tool import create_project
from tools.Projects.delete_project_tool import delete_project

REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")


def test_delete_project():
    """Normal case test for Redmine project deletion API

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    identifier = random_identifier()
    name = "Project for deletion test_" + identifier

    # Create project
    result_create = create_project(
        name=name,
        identifier=identifier,
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
        description="Project for deletion test",
    )
    pprint(result_create, stream=sys.stderr)
    assert isinstance(result_create, dict)
    assert "id" in result_create
    assert result_create["identifier"] == identifier

    # Delete project
    result_delete = delete_project(
        project_id_or_identifier=identifier,
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
    )
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "success"


def test_delete_nonexistent_project():
    """Test for deleting a non-existent Redmine project API

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    # Specify a non-existent project ID
    nonexistent_id = "nonexistent_project_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=8),
    )

    # Delete project
    result_delete = delete_project(
        project_id_or_identifier=nonexistent_id,
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
    )
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "error"
    assert "status_code" in result_delete
