from fastmcp.tools.tool import Tool

from tools.Users.delete_user import delete_user

DeleteUserTool = Tool.from_function(
    delete_user,
    name="delete_user",
    description="Delete a user in Redmine by user_id.",
)
