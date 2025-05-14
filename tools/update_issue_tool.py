import requests
from fastmcp.tools.tool import Tool


def update_issue(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    subject: str = None,
    description: str = None,
    custom_fields=None,
    uploads=None,
):
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
    return {
        "success": resp.status_code in (200, 204),
        "status_code": resp.status_code,
        "response_text": resp.text,
    }


UpdateIssueTool = Tool.from_function(update_issue, name="update_issue", description="Update an existing issue in Redmine.")
