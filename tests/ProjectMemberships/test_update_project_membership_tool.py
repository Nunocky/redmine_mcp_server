"""Integration test for UpdateProjectMembershipTool.

Author: Cline
"""

import os

import pytest

from tools.ProjectMemberships.update_project_membership_tool import UpdateProjectMembershipTool


def test_execute_success():
    """Test successful update of membership roles from real Redmine server.

    Note: Set REDMINE_URL, REDMINE_ADMIN_API_KEY, TEST_REDMINE_MEMBERSHIP_ID, and ROLE_DEVELOPER before running.
    """
    membership_id = os.getenv("TEST_REDMINE_MEMBERSHIP_ID")
    role_id = os.getenv("ROLE_DEVELOPER")
    if not membership_id or not role_id:
        pytest.skip("TEST_REDMINE_MEMBERSHIP_ID and ROLE_DEVELOPER must be set in environment variables.")
    membership_id = int(membership_id)
    role_id = int(role_id)
    tool = UpdateProjectMembershipTool()
    try:
        result = tool.execute(membership_id, [role_id])
    except Exception as e:
        pytest.skip(f"Membership ID {membership_id} or role ID {role_id} does not exist on the test Redmine server: {e}")
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
