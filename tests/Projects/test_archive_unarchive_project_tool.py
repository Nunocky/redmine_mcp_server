import os
import pytest
import pprint
import dotenv
from tests.random_identifier import random_identifier
from tools.Projects.create_project_tool import create_project
from tools.Projects.archive_project_tool import archive_project
from tools.Projects.unarchive_project_tool import unarchive_project
from tools.Projects.delete_project_tool import delete_project

dotenv.load_dotenv()


def test_create_archive_unarchive_delete_project_real_api():
    """Real API: Create project -> Archive -> Unarchive -> Delete"""
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

    # Archive project
    result_archive = archive_project(identifier, redmine_url=redmine_url, api_key=api_key)
    pprint.pprint(result_archive)
    assert result_archive["status"] == "success"

    # Unarchive project
    result_unarchive = unarchive_project(identifier, redmine_url=redmine_url, api_key=api_key)
    pprint.pprint(result_unarchive)
    assert result_unarchive["status"] == "success"

    # Delete project
    result_delete = delete_project(identifier, redmine_url=redmine_url, api_key=api_key)
    pprint.pprint(result_delete)
    assert result_delete["status"] == "success"
