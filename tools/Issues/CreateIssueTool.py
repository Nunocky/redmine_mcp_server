from fastmcp.tools.tool import Tool

from tools.Issues.create_issue_tool import create_issue

CreateIssueTool = Tool.from_function(
    create_issue,
    name="create_issue",
    description="Create a new issue in Redmine.",
)
