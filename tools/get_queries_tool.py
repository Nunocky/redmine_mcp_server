import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetQueriesTool(MCPTool):
    name = "get_queries"
    description = "Get a list of queries from Redmine."
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
    ]
    output = MCPToolOutput(
        type="object",
        properties={
            "queries": {
                "type": "array",
                "description": "List of queries",
                "items": {"type": "object"},
            },
        },
        required=["queries"],
    )

    def run(self, redmine_url, api_key):
        import os

        if redmine_url is None:
            redmine_url = os.environ.get("REDMINE_URL")
        if api_key is None:
            api_key = os.environ.get("REDMINE_API_KEY")
        headers = {"X-Redmine-API-Key": api_key}
        url = f"{redmine_url.rstrip('/')}/queries.json"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return {
            "queries": data.get("queries", []),
        }
