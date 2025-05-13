import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class GetWikiPagesTool(MCPTool):
    name = "get_wiki_pages"
    description = "Get a list of wiki pages from Redmine."
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
            description="Project ID (required)",
            required=True,
        ),
    ]
    output = MCPToolOutput(
        type="object",
        properties={
            "wiki_pages": {
                "type": "array",
                "description": "List of wiki pages",
                "items": {"type": "object"},
            },
        },
        required=["wiki_pages"],
    )

    def run(self, redmine_url, api_key, project_id):
        import os

        if redmine_url is None:
            redmine_url = os.environ.get("REDMINE_URL")
        if api_key is None:
            api_key = os.environ.get("REDMINE_API_KEY")
        headers = {"X-Redmine-API-Key": api_key}
        url = f"{redmine_url.rstrip('/')}/projects/{project_id}/wiki/index.json"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return {
            "wiki_pages": data.get("wiki_pages", []),
        }
