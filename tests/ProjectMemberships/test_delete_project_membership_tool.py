"""Integration test for DeleteProjectMembershipTool."""

import os

from tools.ProjectMemberships.delete_project_membership_tool import DeleteProjectMembershipTool


def test_execute_success():
    """Test successful deletion of membership from real Redmine server.

    This test creates a membership, then deletes it.
    """
    from tools.ProjectMemberships.create_membership_tool import create_membership

    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    project_id = os.getenv("REDMINE_TEST_PROJECT_ID")
    user_id = int(os.getenv("REDMINE_USER_ID", "0"))
    # テスト用ロールID（例: 開発者ロール）
    role_ids = [int(os.getenv("ROLE_DEVELOPER"))]

    # 事前にmembershipを作成
    create_result = create_membership(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
        user_id=user_id,
        role_ids=role_ids,
    )
    assert "membership" in create_result, f"Failed to create membership: {create_result}"
    membership_id = create_result["membership"]["id"]

    tool = DeleteProjectMembershipTool()
    result = tool.execute(membership_id)
    assert result["status"] == "success"
    assert result["status_code"] == 204


def test_execute_not_found():
    """Test deletion with non-existent membership_id from real Redmine server."""
    tool = DeleteProjectMembershipTool()
    # 9999999 is assumed to not exist
    result = tool.execute(9999999)
    assert result["status"] == "failed"
    assert result["status_code"] != 204
