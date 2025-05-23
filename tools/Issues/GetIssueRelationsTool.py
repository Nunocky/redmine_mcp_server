from fastmcp.tools.tool import Tool

from tools.Issues.get_issue_relations import get_issue_relations

GetIssueRelationsTool = Tool.from_function(
    get_issue_relations,
    name="get_issue_relations",
    description="Redmineの課題リレーション一覧を取得します。",
)
