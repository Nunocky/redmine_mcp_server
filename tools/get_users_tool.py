import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetUsersTool(MCPTool):
    name = "get_users"
    description = "Get a list of users from Redmine."
    arguments = [
        MCPToolArgument(
            name="redmine_url",
            type="string",
            description="Base URL of Redmine (e.g. https://redmine.example.com)",
            required=True,
        ),
        MCPToolArgument(
            name="api_key",
            type="string",
            description="Redmine API key",
            required=True,
        ),
        MCPToolArgument(
            name="limit",
            type="integer",
            description="Number of items to retrieve (pagination)",
            required=False,
        ),
        MCPToolArgument(
            name="offset",
            type="integer",
            description="Offset for pagination",
            required=False,
        ),
    ]
    output = MCPToolOutput(
        type="object",
        properties={
            "users": {
                "type": "array",
                "description": "List of users",
                "items": {"type": "object"},
            },
            "total_count": {"type": "integer", "description": "Total number of users"},
            "limit": {"type": "integer", "description": "Number of items returned"},
            "offset": {"type": "integer", "description": "Offset of the first item returned"},
        },
        required=["users", "total_count", "limit", "offset"],
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
