import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetTimeEntriesTool(MCPTool):
    name = "get_time_entries"
    description = "Get a list of time entries from Redmine."
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
            name="project_id",
            type="string",
            description="Project ID (if omitted, all projects)",
            required=False,
        ),
        MCPToolArgument(
            name="user_id",
            type="integer",
            description="User ID (if omitted, all users)",
            required=False,
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
            "time_entries": {
                "type": "array",
                "description": "List of time entries",
                "items": {"type": "object"},
            },
            "total_count": {"type": "integer", "description": "Total number of time entries"},
            "limit": {"type": "integer", "description": "Number of items returned"},
            "offset": {"type": "integer", "description": "Offset of the first item returned"},
        },
        required=["time_entries", "total_count", "limit", "offset"],
    )

    def run(self, redmine_url, api_key, project_id=None, user_id=None, limit=None, offset=None):
        import os

        if redmine_url is None:
            redmine_url = os.environ.get("REDMINE_URL")
        if api_key is None:
            api_key = os.environ.get("REDMINE_API_KEY")
        headers = {"X-Redmine-API-Key": api_key}
        params = {}
        if project_id:
            params["project_id"] = project_id
        if user_id is not None:
            params["user_id"] = user_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        url = f"{redmine_url.rstrip('/')}/time_entries.json"
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return {
            "time_entries": data.get("time_entries", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
