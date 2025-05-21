from fastmcp.tools.tool import Tool

from tools.Users.update_user_tool import update_user

UpdateUserTool = Tool.from_function(
    update_user,
    name="update_user",
    description="Update a user in Redmine by user_id.",
)
