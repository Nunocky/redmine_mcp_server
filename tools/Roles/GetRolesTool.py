from fastmcp.tools.tool import Tool

from tools.Roles.get_roles import get_roles

GetRolesTool = Tool.from_function(
    get_roles,
    name="get_roles",
    description="Get the list of roles from Redmine.",
)
