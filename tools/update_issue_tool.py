import requests
from fastmcp.server import MCPTool, MCPToolArgument, MCPToolOutput


class UpdateIssueTool(MCPTool):
    name = "update_issue"
    description = "Update an existing issue in Redmine."
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
            description="ID of the issue to update",
            required=True,
        ),
        MCPToolArgument(
            name="subject",
            type="string",
            description="Issue subject/title",
            required=False,
        ),
        MCPToolArgument(
            name="description",
            type="string",
            description="Issue description",
            required=False,
        ),
        MCPToolArgument(
            name="custom_fields",
            type="array",
            description="Custom fields (e.g. [{'id':1,'value':'foo'}])",
            required=False,
        ),
        MCPToolArgument(
            name="uploads",
            type="array",
            description="Attachment info (e.g. [{'token':'xxx','filename':'a.txt'}])",
            required=False,
        ),
    ]
    output = MCPToolOutput(
        type="object",
        properties={"success": {"type": "boolean", "description": "Update success flag"}},
        required=["success"],
    )

    def run(self, redmine_url, api_key, issue_id, subject=None, description=None, custom_fields=None, uploads=None):
        import os

        if redmine_url is None:
            redmine_url = os.environ.get("REDMINE_URL")
        if api_key is None:
            api_key = os.environ.get("REDMINE_API_KEY")
        headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
        issue_data = {}
        if subject:
            issue_data["subject"] = subject
        if description:
            issue_data["description"] = description
        if custom_fields:
            issue_data["custom_fields"] = custom_fields
        if uploads:
            issue_data["uploads"] = uploads
        url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
        resp = requests.put(url, headers=headers, json={"issue": issue_data})
        resp.raise_for_status()
        return {"success": resp.status_code == 200}
