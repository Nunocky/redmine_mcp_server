"""Redmine User Deletion Tool

Delete a user using RedmineAPIClient.
404エラー時はException送出、204時は{"success": True}返却、他エラーも例外送出。

Returns:
    dict: {"success": True} if deleted (204)

Raises:
    Exception: When API request fails (including 404 errors)
"""

from typing import Any, Dict

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def delete_user(
    redmine_url: str,
    api_key: str,
    user_id: int,
) -> Dict[str, Any]:
    """Delete a user in Redmine by user_id

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        user_id: User ID to delete

    Returns:
        {"success": True} if deleted (204)

    Raises:
        Exception: When API request fails (including 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/users/{user_id}.json"
    resp = client.delete(endpoint)
    if resp.status_code == 204:
        return {"success": True}
    # 204以外はraise_for_statusで例外送出（404含む）
    resp.raise_for_status()


DeleteUserTool = Tool.from_function(
    delete_user,
    name="delete_user",
    description="Delete a user in Redmine by user_id.",
)
