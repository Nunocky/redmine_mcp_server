from fastmcp.tools.tool import Tool
from tools.Groups.update_group import update_group

UpdateGroupTool = Tool.from_function(
    update_group,
    name="update_group",
    description="Update a Redmine group (PUT /groups/{id}.json). Returns updated group info. 404 returns {'group': None}.",
)
