"""Integration test for GetProjectMembershipTool."""

import os

import pytest

from tools.ProjectMemberships.get_project_membership_tool import GetProjectMembershipTool
from tools.redmine_api_client import RedmineAPIClient


def test_execute_success():
    """Test successful retrieval of membership detail from real Redmine server.

    Note: Set REDMINE_URL, REDMINE_API_KEY, and a valid membership_id before running.
    """
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    tool = GetProjectMembershipTool(
        client=RedmineAPIClient(redmine_url, api_key),
    )

    # get membership id from projects/{project_id}/memberships.json
    project_id = int(os.getenv("REDMINE_TEST_PROJECT_ID"))
    path = f"/projects/{project_id}/memberships.json"
    resp = tool.client.get(path)
    data = resp.json()
    membership_id = data["memberships"][0]["id"]
    if not membership_id:
        raise ValueError("No membership ID found in the response.")

    result = tool.execute(membership_id)
    assert result["id"] == membership_id
    assert "project" in result
    assert "user" in result or "group" in result
    assert "roles" in result


def test_execute_not_found():
    """Test retrieval with non-existent membership_id from real Redmine server."""
    tool = GetProjectMembershipTool()
    # 9999999 is assumed to not exist
    with pytest.raises(Exception) as excinfo:
        tool.execute(9999999)
    assert "Failed to get project membership detail" in str(excinfo.value)
