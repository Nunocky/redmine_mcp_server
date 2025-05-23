from fastmcp.tools.tool import Tool

from tools.IssueCategories.get_issue_categories import get_issue_categories

GetIssueCategoriesTool = Tool.from_function(
    get_issue_categories,
    name="get_issue_categories",
    description="Get Redmine issue categories for a project.",
)
