from fastmcp.tools.tool import Tool

from tools.ProjectMemberships.get_project_membership import get_project_membership

GetProjectMembershipTool = Tool.from_function(
    get_project_membership,
    name="get_project_membership",
    description="Get the details of a project membership from Redmine.",
)
