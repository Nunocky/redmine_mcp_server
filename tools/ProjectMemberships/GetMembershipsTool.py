from fastmcp.tools.tool import Tool

from tools.ProjectMemberships.get_memberships_tool import get_memberships

GetMembershipsTool = Tool.from_function(
    get_memberships,
    name="get_memberships",
    description="Get a list of Redmine project memberships",
)
