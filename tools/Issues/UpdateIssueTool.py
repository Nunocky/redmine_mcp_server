import requests
from fastmcp.tools.tool import Tool

from tools.Issues.update_issue import update_issue

UpdateIssueTool = Tool.from_function(
    update_issue,
    name="update_issue",
    description="Update an existing issue in Redmine.",
)
