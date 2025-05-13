import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetUsersTool(MCPTool):
    name = "get_users"
    description = "Redmineのユーザー一覧を取得します"
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
            "users": {
                "type": "array",
                "description": "ユーザー一覧",
                "items": {"type": "object"},
            },
            "total_count": {"type": "integer", "description": "全ユーザー数"},
            "limit": {"type": "integer", "description": "取得件数"},
            "offset": {"type": "integer", "description": "取得開始位置"},
        },
        required=["users", "total_count", "limit", "offset"],
    )

    def run(self, redmine_url, api_key, limit=None, offset=None):
        headers = {"X-Redmine-API-Key": api_key}
        params = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        url = f"{redmine_url.rstrip('/')}/users.json"
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return {
            "users": data.get("users", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
