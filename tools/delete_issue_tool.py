import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class DeleteIssueTool(MCPTool):
    name = "delete_issue"
    description = "Delete an issue from Redmine."
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
            type="integer",
            description="ID of the issue to delete",
            required=True,
        ),
    ]
    output = MCPToolOutput(
        type="object",
        properties={"success": {"type": "boolean", "description": "Delete success flag"}},
        required=["success"],
    )

    def run(self, redmine_url, api_key, issue_id):
        import os

        if redmine_url is None:
            redmine_url = os.environ.get("REDMINE_URL")
        if api_key is None:
            api_key = os.environ.get("REDMINE_API_KEY")
        headers = {"X-Redmine-API-Key": api_key}
        url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
        resp = requests.delete(url, headers=headers)
        resp.raise_for_status()
        return {"success": resp.status_code == 200}
