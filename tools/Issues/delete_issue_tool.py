import requests
from fastmcp.tools.tool import Tool


def delete_issue(redmine_url: str, api_key: str, issue_id: int):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
    resp = requests.delete(url, headers=headers)
    resp.raise_for_status()
    return {"success": resp.status_code in (200, 204)}


DeleteIssueTool = Tool.from_function(delete_issue, name="delete_issue", description="Delete an issue from Redmine.")
