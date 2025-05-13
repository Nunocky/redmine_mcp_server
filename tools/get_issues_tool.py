import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetIssuesTool(MCPTool):
    name = "get_issues"
    description = "Redmineの課題一覧を取得します"
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
            description="プロジェクトID（省略時は全プロジェクト）",
            required=False,
        ),
        MCPToolArgument(
            name="limit",
            type="integer",
            description="取得件数（ページネーション用）",
            required=False,
        ),
        MCPToolArgument(
            name="offset",
            type="integer",
            description="取得開始位置（ページネーション用）",
            required=False,
        ),
    ]
    output = MCPToolOutput(
        type="object",
        properties={
            "issues": {
                "type": "array",
                "description": "課題一覧",
                "items": {"type": "object"},
            },
            "total_count": {"type": "integer", "description": "全課題数"},
            "limit": {"type": "integer", "description": "取得件数"},
            "offset": {"type": "integer", "description": "取得開始位置"},
        },
        required=["issues", "total_count", "limit", "offset"],
    )

    def run(self, redmine_url, api_key, project_id=None, limit=None, offset=None):
        headers = {"X-Redmine-API-Key": api_key}
        params = {}
        if project_id:
            params["project_id"] = project_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        url = f"{redmine_url.rstrip('/')}/issues.json"
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return {
            "issues": data.get("issues", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
