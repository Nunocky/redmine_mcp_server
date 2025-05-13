import requests
from fastmcp.tools.tool import Tool


def create_issue(
    redmine_url: str, api_key: str, project_id: str, subject: str, description: str = None, custom_fields=None, uploads=None
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
    issue_data = {
        "project_id": project_id,
        "subject": subject,
    }
    if description:
        issue_data["description"] = description
    if custom_fields:
        issue_data["custom_fields"] = custom_fields
    if uploads:
        issue_data["uploads"] = uploads
    url = f"{redmine_url.rstrip('/')}/issues.json"
    resp = requests.post(url, headers=headers, json={"issue": issue_data})
    resp.raise_for_status()
    return {"issue": resp.json().get("issue", {})}


CreateIssueTool = Tool.from_function(create_issue, name="create_issue", description="Create a new issue in Redmine.")
