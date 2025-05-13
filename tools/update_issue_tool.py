import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class UpdateIssueTool(MCPTool):
    name = "update_issue"
    description = "Redmineの課題を更新します"
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
            description="更新対象の課題ID",
            required=True,
        ),
        MCPToolArgument(
            name="subject",
            type="string",
            description="課題タイトル",
            required=False,
        ),
        MCPToolArgument(
            name="description",
            type="string",
            description="課題の説明",
            required=False,
        ),
        MCPToolArgument(
            name="custom_fields",
            type="array",
            description="カスタムフィールド（例: [{'id':1,'value':'foo'}]）",
            required=False,
        ),
        MCPToolArgument(
            name="uploads",
            type="array",
            description="添付ファイル情報（例: [{'token':'xxx','filename':'a.txt'}]）",
            required=False,
        ),
    ]
    output = MCPToolOutput(
        type="object",
        properties={"success": {"type": "boolean", "description": "更新成功フラグ"}},
        required=["success"],
    )

    def run(self, redmine_url, api_key, issue_id, subject=None, description=None, custom_fields=None, uploads=None):
        headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
        issue_data = {}
        if subject:
            issue_data["subject"] = subject
        if description:
            issue_data["description"] = description
        if custom_fields:
            issue_data["custom_fields"] = custom_fields
        if uploads:
            issue_data["uploads"] = uploads
        url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
        resp = requests.put(url, headers=headers, json={"issue": issue_data})
        resp.raise_for_status()
        return {"success": resp.status_code == 200}
