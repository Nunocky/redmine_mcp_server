"""Function for deleting a project membership in Redmine.

This function uses DeleteProjectMembershipTool to delete a specific membership.
"""

from tools.ProjectMemberships.DeleteProjectMembershipTool import DeleteProjectMembershipTool


def delete_project_membership(membership_id: int) -> dict:
    """Delete a project membership by ID.

    Args:
        membership_id (int): The ID of the membership to delete.

    Returns:
        dict: Result with status code or error message.
    """
    tool = DeleteProjectMembershipTool()
    return tool.execute(membership_id)
