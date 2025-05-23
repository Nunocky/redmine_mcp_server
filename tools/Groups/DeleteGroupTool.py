from fastmcp.tools.tool import Tool

from tools.Groups.delete_group import delete_group

DeleteGroupTool = Tool.from_function(
    delete_group,
    name="delete_group",
    description="Delete a Redmine group (DELETE /groups/{id}.json). Returns {'success': True} if deleted, {'success': False, 'error': 'Not found'} for 404.",
)
