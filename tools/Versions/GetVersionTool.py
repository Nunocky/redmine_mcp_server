from fastmcp.tools.tool import Tool

from tools.Versions.get_versions_tool import get_versions

GetVersionTool = Tool.from_function(
    get_versions,
    name="get_versions",
    description="Get versions from Redmine",
)
