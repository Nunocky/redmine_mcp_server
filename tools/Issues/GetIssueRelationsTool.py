from fastmcp.tools.tool import Tool

from tools.Issues.get_issue_relations_tool import get_issue_relations

GetIssueRelationsTool = Tool.from_function(
    get_issue_relations,
    name="get_issue_relations",
    description="Get a list of Redmine issue relations",
)
