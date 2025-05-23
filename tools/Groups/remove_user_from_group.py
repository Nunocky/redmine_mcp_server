from typing import Any, Dict

import requests

from tools.redmine_api_client import RedmineAPIClient


def remove_user_from_group(
    redmine_url: str,
    api_key: str,
    group_id: int,
    user_id: int,
) -> Dict[str, Any]:
    """Remove a user from a Redmine group.

    Args:
        redmine_url (str): Base URL of Redmine.
        api_key (str): Redmine API key.
        group_id (int): Group ID.
        user_id (int): User ID to remove.

    Returns:
        Dict[str, Any]: {"success": True} if deleted, {"success": False, "error": "Not found"} for 404.

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    try:
        response = client.delete(
            endpoint=f"/groups/{group_id}/users/{user_id}.json",
        )
        if response.status_code == 204:
            return {"success": True}
        return {"success": False, "error": "Unexpected response"}
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"success": False, "error": "Not found"}
        return {"success": False, "error": str(e)}
