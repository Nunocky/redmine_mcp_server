"""Tool to remove a watcher from a Redmine issue"""

import requests
from fastmcp.tools.tool import Tool


def remove_watcher(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    user_id: int,
):
    """
    Remove a watcher (user_id) from the specified issue (issue_id)

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        issue_id (int): Issue ID
        user_id (int): User ID to remove

    Returns:
        dict: Success status and response information
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}/watchers/{user_id}.json"
    resp = requests.delete(url, headers=headers)
    return {
        "success": resp.status_code in (200, 204),
        "status_code": resp.status_code,
        "response_text": resp.text,
    }


RemoveWatcherTool = Tool.from_function(
    remove_watcher,
    name="remove_watcher",
    description="Remove a watcher from a Redmine issue",
)
