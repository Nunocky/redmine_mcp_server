"""Integration test for UpdateProjectMembershipTool.

Author: Cline
"""

import os

import pytest

from tools.ProjectMemberships.update_project_membership_tool import UpdateProjectMembershipTool


def test_execute_success():
    """Test successful update of membership roles from real Redmine server.

    Note: Set REDMINE_URL, REDMINE_ADMIN_API_KEY, TEST_REDMINE_MEMBERSHIP_ID, and TEST_REDMINE_ROLE_ID before running.
    """
    membership_id = int(os.getenv("TEST_REDMINE_MEMBERSHIP_ID"))
    role_id = int(os.getenv("ROLE_DEVELOPER"))
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
