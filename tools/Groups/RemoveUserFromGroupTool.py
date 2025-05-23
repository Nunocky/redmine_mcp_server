from fastmcp.tools.tool import Tool

from tools.Groups.remove_user_from_group import remove_user_from_group

RemoveUserFromGroupTool = Tool.from_function(
    remove_user_from_group,
    name="remove_user_from_group",
    description="Redmineグループからユーザーを削除します（DELETE /groups/{id}/users/{user_id}.json）。返り値は Dict[str, Any] 型で、{'success': True}（削除成功）、{'success': False, 'error': 'Not found'}（404時）などを返します。",
)
