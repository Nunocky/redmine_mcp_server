from fastmcp.tools.tool import Tool

from tools.Roles.get_role_tool import get_role

GetRoleTool = Tool.from_function(
    get_role,
    name="get_role",
    description="Get the detail of a specific role from Redmine.",
)
