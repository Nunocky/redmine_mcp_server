import requests
from tools.redmine_api_client import RedmineAPIClient


def add_user_to_group(
    redmine_url: str,
    api_key: str,
    group_id: int,
    user_ids: list,
):
    """Add users to a Redmine group.

    Args:
        redmine_url (str): Base URL of Redmine.
        api_key (str): Redmine API key.
        group_id (int): Group ID.
        user_ids (list): List of user IDs to add.

    Returns:
        dict: {"success": True} if added, {"success": False, "error": "Not found"} for 404.

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    data = {"user_ids": user_ids}
    try:
        response = client.post(
            endpoint=f"/groups/{group_id}/users.json",
            json=data,
        )
        if response.status_code in (200, 201, 204):
            return {"success": True}
        return {"success": False, "error": "Unexpected response"}
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"success": False, "error": "Not found"}
        raise
