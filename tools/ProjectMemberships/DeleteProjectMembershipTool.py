from fastmcp.tools.tool import Tool

from tools.ProjectMemberships.delete_project_membership import delete_project_membership

DeleteProjectMembershipTool = Tool.from_function(
    delete_project_membership,
    name="delete_project_membership",
    description="Delete a project membership by ID in Redmine.",
)
