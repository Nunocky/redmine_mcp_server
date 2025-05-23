from fastmcp.tools.tool import Tool
from tools.Groups.get_groups import get_groups

GetGroupsTool = Tool.from_function(
    get_groups,
    name="get_groups",
    description="Get Redmine groups list (GET /groups.json). Returns groups list and page info. 404 returns empty list.",
)
