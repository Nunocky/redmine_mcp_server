from fastmcp.tools.tool import Tool

from tools.ProjectMemberships.update_project_membership import update_project_membership

UpdateProjectMembershipTool = Tool.from_function(
    update_project_membership,
    name="update_project_membership",
    description="Update the roles of a project membership in Redmine.",
)
