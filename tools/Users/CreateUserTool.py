from fastmcp.tools.tool import Tool

from tools.Users.create_user_tool import create_user

CreateUserTool = Tool.from_function(
    create_user,
    name="create_user",
    description="Create a new user in Redmine.",
)
