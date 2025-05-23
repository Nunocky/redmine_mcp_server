from fastmcp.tools.tool import Tool

from tools.Issues.delete_issue_relation import delete_issue_relation

DeleteIssueRelationTool = Tool.from_function(
    delete_issue_relation,
    name="delete_issue_relation",
    description="Redmineの課題リレーションを削除します。",
)
