"""Tool to add a watcher to a Redmine issue"""

import requests
from fastmcp.tools.tool import Tool


def add_watcher(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    user_id: int,
):
    """
    Add a watcher (user_id) to the specified issue (issue_id)

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        issue_id (int): Issue ID
        user_id (int): User ID to add

    Returns:
        dict: Success status and response information
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}/watchers.json"
    data = {"user_id": user_id}
    resp = requests.post(url, headers=headers, json=data)
    return {
        "success": resp.status_code in (200, 201, 204),
        "status_code": resp.status_code,
        "response_text": resp.text,
    }


AddWatcherTool = Tool.from_function(
    add_watcher,
    name="add_watcher",
    description="Add a watcher to a Redmine issue",
)
