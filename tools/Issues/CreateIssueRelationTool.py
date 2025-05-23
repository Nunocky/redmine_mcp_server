from fastmcp.tools.tool import Tool

from tools.Issues.create_issue_relation import create_issue_relation

CreateIssueRelationTool = Tool.from_function(
    create_issue_relation,
    name="create_issue_relation",
    description="Redmineに課題リレーションを新規作成します。",
)
