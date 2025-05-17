import os
import pytest
import pprint
import dotenv
from tools.Projects.get_project_tool import get_project

dotenv.load_dotenv()


def test_get_project_by_id_real_api():
    """Real API: Get details by project ID"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_PROJECT_ID")
    print(f"REDMINE_URL={redmine_url}, REDMINE_ADMIN_API_KEY={'***' if api_key else ''}, REDMINE_PROJECT_ID={project_id}")
    if not redmine_url or not api_key or not project_id:
        pytest.skip("Skipping because REDMINE_URL, REDMINE_ADMIN_API_KEY, and REDMINE_PROJECT_ID are not set")
    result = get_project(project_id, redmine_url, api_key)
    pprint.pprint(result)
    assert "id" in result
    assert "name" in result


def test_get_project_by_identifier_real_api():
    """Real API: Get details by project identifier"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_identifier = os.environ.get("REDMINE_PROJECT_IDENTIFIER")
    print(
        f"REDMINE_URL={redmine_url}, REDMINE_ADMIN_API_KEY={'***' if api_key else ''}, REDMINE_PROJECT_IDENTIFIER={project_identifier}"
    )
    if not redmine_url or not api_key or not project_identifier:
        pytest.skip("Skipping because REDMINE_URL, REDMINE_ADMIN_API_KEY, and REDMINE_PROJECT_IDENTIFIER are not set")
    result = get_project(project_identifier, redmine_url, api_key)
    pprint.pprint(result)
    assert "id" in result
    assert "name" in result


def test_get_project_with_include_real_api():
    """Real API: Get details with include parameter specified"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_PROJECT_ID")
    print(f"REDMINE_URL={redmine_url}, REDMINE_ADMIN_API_KEY={'***' if api_key else ''}, REDMINE_PROJECT_ID={project_id}")
    if not redmine_url or not api_key or not project_id:
        pytest.skip("Skipping because REDMINE_URL, REDMINE_ADMIN_API_KEY, and REDMINE_PROJECT_ID are not set")
    result = get_project(project_id, redmine_url, api_key, include="trackers,enabled_modules")
    pprint.pprint(result)
    assert "id" in result
    assert "name" in result
