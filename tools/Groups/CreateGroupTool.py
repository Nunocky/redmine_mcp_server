from fastmcp.tools.tool import Tool
from tools.Groups.create_group import create_group

CreateGroupTool = Tool.from_function(
    create_group,
    name="create_group",
    description="Create a Redmine group (POST /groups.json). Returns created group info.",
)
