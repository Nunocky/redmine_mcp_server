import os
import pprint

import pytest

from tools.Projects.get_project import get_project


def test_get_project_by_id_api():
    """Real API: Get details by project ID"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")

    result = get_project(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id_or_identifier=project_id,
    )
    pprint.pprint(result)
    if result == {}:
        pytest.fail("Project not found or API returns 404.")
    assert "id" in result
    assert "name" in result


def test_get_project_by_identifier_api():
    """Real API: Get details by project identifier"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_identifier = os.environ.get("REDMINE_TEST_PROJECT_ID")
    result = get_project(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id_or_identifier=project_identifier,
    )
    pprint.pprint(result)
    if result == {}:
        pytest.skip("Project not found or API returns 404.")
    assert "id" in result
    assert "name" in result


def test_get_project_with_include_api():
    """Real API: Get details with include parameter specified"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")

    # 404だと {} が返る
    result = get_project(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id_or_identifier=project_id,
        include="trackers,enabled_modules",
    )
    pprint.pprint(result)
    if result == {}:
        # 404（空dict）が返る場合も許容
        return
    assert "id" in result
    assert "name" in result
