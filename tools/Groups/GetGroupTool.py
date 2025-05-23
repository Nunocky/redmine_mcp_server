from fastmcp.tools.tool import Tool
from tools.Groups.get_group import get_group

GetGroupTool = Tool.from_function(
    get_group,
    name="get_group",
    description="Get Redmine group detail (GET /groups/{id}.json). Returns group detail info. 404 returns {'group': None}.",
)
