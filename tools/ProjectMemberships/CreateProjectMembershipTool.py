from fastmcp.tools.tool import Tool

from tools.ProjectMemberships.create_membership_tool import create_membership

CreateProjectMembershipTool = Tool.from_function(
    create_membership,
    name="create_project_membership",
    description="Create a new project membership in Redmine",
)
