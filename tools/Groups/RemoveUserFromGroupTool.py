from fastmcp.tools.tool import Tool

from tools.Groups.remove_user_from_group import remove_user_from_group

RemoveUserFromGroupTool = Tool.from_function(
    remove_user_from_group,
    name="remove_user_from_group",
    description="Remove a user from a Redmine group (DELETE /groups/{id}/users/{user_id}.json). Returns {'success': True} if deleted, {'success': False, 'error': 'Not found'} for 404.",
)
