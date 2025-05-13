import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetIssueRelationsTool(MCPTool):
    name = "get_issue_relations"
    description = "Get a list of issue relations from Redmine."
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
            name="issue_id",
            type="string",
            description="Issue ID (if omitted, all relations)",
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
            "relations": {
                "type": "array",
                "description": "List of issue relations",
                "items": {"type": "object"},
            },
            "total_count": {"type": "integer", "description": "Total number of relations"},
            "limit": {"type": "integer", "description": "Number of items returned"},
            "offset": {"type": "integer", "description": "Offset of the first item returned"},
        },
        required=["relations", "total_count", "limit", "offset"],
    )

    def run(self, redmine_url, api_key, issue_id=None, limit=None, offset=None):
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
        if issue_id:
            url = f"{redmine_url.rstrip('/')}/issues/{issue_id}/relations.json"
        else:
            url = f"{redmine_url.rstrip('/')}/relations.json"
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        return {
            "relations": data.get("relations", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
