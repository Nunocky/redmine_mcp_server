from fastmcp.tools.tool import Tool

from tools.Issues.get_issues_tool import get_issues

GetIssuesTool = Tool.from_function(
    get_issues,
    name="get_issues",
    description="Get a list of Redmine issues",
)
