import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class DeleteIssueTool(MCPTool):
    name = "delete_issue"
    description = "Redmineの課題を削除します"
    arguments = [
        MCPToolArgument(
            name="redmine_url",
            type="string",
            description="RedmineのベースURL（例: https://redmine.example.com）",
            required=True,
        ),
        MCPToolArgument(
            name="api_key",
            type="string",
            description="RedmineのAPIキー",
            required=True,
        ),
        MCPToolArgument(
            name="issue_id",
            type="integer",
            description="削除対象の課題ID",
            required=True,
        ),
    ]
    output = MCPToolOutput(
        type="object",
        properties={"success": {"type": "boolean", "description": "削除成功フラグ"}},
        required=["success"],
    )

    def run(self, redmine_url, api_key, issue_id):
        headers = {"X-Redmine-API-Key": api_key}
        url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        return {"success": resp.status_code == 200}
