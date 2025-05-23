from fastmcp.tools.tool import Tool
from tools.Groups.add_user_to_group import add_user_to_group

AddUserToGroupTool = Tool.from_function(
    add_user_to_group,
    name="add_user_to_group",
    description="Add users to a Redmine group (POST /groups/{id}/users.json). Returns {'success': True} if added, {'success': False, 'error': 'Not found'} for 404.",
)
