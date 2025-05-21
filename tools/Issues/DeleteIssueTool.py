from fastmcp.tools.tool import Tool

from tools.Issues.delete_issue import delete_issue

DeleteIssueTool = Tool.from_function(
    delete_issue,
    name="delete_issue",
    description="Delete an issue from Redmine.",
)
