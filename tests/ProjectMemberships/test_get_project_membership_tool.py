"""Integration test for GetProjectMembershipTool.

Author: Cline
"""

import os

import pytest

from tools.ProjectMemberships.get_project_membership_tool import GetProjectMembershipTool


def test_execute_success():
    """Test successful retrieval of membership detail from real Redmine server.

    Note: Set REDMINE_URL, REDMINE_API_KEY, and a valid membership_id before running.
    """
    membership_id = int(os.getenv("TEST_REDMINE_MEMBERSHIP_ID"))
    tool = GetProjectMembershipTool()
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
