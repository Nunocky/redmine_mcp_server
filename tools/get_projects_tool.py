import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetProjectsTool(MCPTool):
    name = "get_projects"
    description = "Redmineのプロジェクト一覧を取得します"
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
            "projects": {
                "type": "array",
                "description": "プロジェクト一覧",
                "items": {"type": "object"},
            },
            "total_count": {"type": "integer", "description": "全プロジェクト数"},
            "limit": {"type": "integer", "description": "取得件数"},
            "offset": {"type": "integer", "description": "取得開始位置"},
        },
        required=["projects", "total_count", "limit", "offset"],
    )

    def run(self, redmine_url, api_key, limit=None, offset=None):
        import os

        if redmine_url is None:
            redmine_url = os.environ.get("REDMINE_URL")
        if api_key is None:
            api_key = os.environ.get("REDMINE_API_KEY")
        headers = {"X-Redmine-API-Key": api_key}
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        url = f"{redmine_url.rstrip('/')}/projects.json"
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return {
            "projects": data.get("projects", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
