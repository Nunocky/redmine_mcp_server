from fastmcp.tools.tool import Tool

from tools.Issues.get_issue import get_issue

GetIssueTool = Tool.from_function(
    get_issue,
    name="get_issue",
    description="Get Redmine issue information",
)
