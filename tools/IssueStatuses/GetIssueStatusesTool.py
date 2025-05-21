from fastmcp.tools.tool import Tool

from tools.IssueStatuses.get_issue_statuses import get_issue_statuses

GetIssueStatusesTool = Tool.from_function(
    get_issue_statuses,
    name="get_issue_statuses",
    description="Get a list of issue statuses from Redmine.",
)
