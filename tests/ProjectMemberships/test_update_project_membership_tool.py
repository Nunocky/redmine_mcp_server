"""Integration test for UpdateProjectMembershipTool.

Author: Cline
"""

import os

import pytest

from tools.ProjectMemberships.get_project_membership_tool import GetProjectMembershipTool
from tools.ProjectMemberships.update_project_membership_tool import UpdateProjectMembershipTool
from tools.redmine_api_client import RedmineAPIClient


def test_execute_success():
    """Test successful update of membership roles from real Redmine server.

    Note: Set REDMINE_URL, REDMINE_ADMIN_API_KEY, TEST_REDMINE_MEMBERSHIP_ID, and ROLE_DEVELOPER before running.
    """
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    project_id = int(os.getenv("REDMINE_TEST_PROJECT_ID"))
    path = f"/projects/{project_id}/memberships.json"
    tool = GetProjectMembershipTool(
        client=RedmineAPIClient(redmine_url, api_key),
    )
    resp = tool.client.get(path)
    data = resp.json()
    membership_id = data["memberships"][0]["id"]
    if not membership_id:
        raise ValueError("No membership ID found in the response.")

    role_id = os.getenv("ROLE_DEVELOPER")
    membership_id = int(membership_id)
    role_id = int(role_id)
    tool = UpdateProjectMembershipTool()
    result = tool.execute(membership_id, [role_id])
    assert result["id"] == membership_id
    assert "roles" in result
    assert any(role["id"] == role_id for role in result["roles"])


def test_execute_not_found():
    """Test update with non-existent membership_id from real Redmine server."""
    tool = UpdateProjectMembershipTool()
    # 9999999 is assumed to not exist
    with pytest.raises(Exception) as excinfo:
        tool.execute(9999999, [1])
    assert "Failed to update project membership" in str(excinfo.value)
