from fastmcp.tools.tool import Tool

from tools.Users.get_user_tool import get_user

GetUserTool = Tool.from_function(
    get_user,
    name="get_user",
    description="Get Redmine user details",
)
