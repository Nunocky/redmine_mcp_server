import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class CreateIssueTool(MCPTool):
    name = "create_issue"
    description = "Redmineの課題を新規作成します"
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
            name="project_id",
            type="string",
            description="プロジェクトID",
            required=True,
        ),
        MCPToolArgument(
            name="subject",
            type="string",
            description="課題タイトル",
            required=True,
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
        properties={"issue": {"type": "object", "description": "作成された課題情報"}},
        required=["issue"],
    )

    def run(self, redmine_url, api_key, project_id, subject, description=None, custom_fields=None, uploads=None):
        import os

        if redmine_url is None:
            redmine_url = os.environ.get("REDMINE_URL")
        if api_key is None:
            api_key = os.environ.get("REDMINE_API_KEY")
        headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
        issue_data = {
            "project_id": project_id,
            "subject": subject,
        }
        if description:
            issue_data["description"] = description
        if custom_fields:
            issue_data["custom_fields"] = custom_fields
        if uploads:
            issue_data["uploads"] = uploads
        url = f"{redmine_url.rstrip('/')}/issues.json"
        resp = requests.post(url, headers=headers, json={"issue": issue_data})
        resp.raise_for_status()
        return {"issue": resp.json().get("issue", {})}
