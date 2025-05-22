from fastmcp.tools.tool import Tool

from tools.Enumerations.get_issue_priorities import get_issue_priorities

GetIssuePrioritiesTool = Tool.from_function(
    get_issue_priorities,
    name="get_issue_priorities",
    description="Retrieves a list of issue priorities from Redmine.",
)
