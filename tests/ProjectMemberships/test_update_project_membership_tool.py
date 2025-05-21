"""Integration test for UpdateProjectMembershipTool."""

import os

import pytest

from tools.ProjectMemberships.get_memberships import get_memberships
from tools.ProjectMemberships.get_project_membership import get_project_membership
from tools.ProjectMemberships.update_project_membership import update_project_membership


def test_execute_success():
    """Test successful update of membership roles from real Redmine server.

    Note: Set REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_TEST_PROJECT_ID, and ROLE_DEVELOPER before running.
    """
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    project_id = os.getenv("REDMINE_TEST_PROJECT_ID")
    role_id = int(os.getenv("ROLE_DEVELOPER"))

    # Get memberships and pick the first one
    memberships_data = get_memberships(redmine_url, api_key, project_id)
    memberships = memberships_data.get("memberships", [])
    if not memberships:
        raise ValueError("No memberships found in the project.")
    membership_id = memberships[0]["id"]

    # Update membership roles
    result = update_project_membership(membership_id, [role_id], redmine_url=redmine_url, api_key=api_key)

    # resultの内容を確認
    assert result["id"] == membership_id
    assert "roles" in result
    assert any(role["id"] == role_id for role in result["roles"])

    # Get membership detail and assert
    membership_detail = get_project_membership(membership_id, redmine_url=redmine_url, api_key=api_key)
    assert membership_detail["id"] == membership_id
    assert "roles" in membership_detail
    assert any(role["id"] == role_id for role in membership_detail["roles"])


def test_execute_not_found():
    """Test update with non-existent membership_id from real Redmine server.

    Note: 9999999 is assumed to not exist.
    """
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    with pytest.raises(Exception) as excinfo:
        update_project_membership(9999999, [1], redmine_url=redmine_url, api_key=api_key)
    assert "Failed to update project membership" in str(excinfo.value)
