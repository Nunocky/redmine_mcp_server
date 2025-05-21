import os
from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


def get_project_membership(
    membership_id: int,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the details of a project membership from Redmine.

    Args:
        membership_id (int): The ID of the membership to retrieve.
        redmine_url (str, optional): The base URL of the Redmine instance.
        api_key (str, optional): The API key for authentication.

    Returns:
        dict: The membership detail information.

    Raises:
        ValueError: If required parameters are missing.
        Exception: When API request fails.
    """
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY") or os.environ.get("REDMINE_USER_API_KEY")
    if not redmine_url or not api_key:
        raise ValueError("redmine_url and api_key are required.")

    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = f"/memberships/{membership_id}.json"
    try:
        resp = client.get(endpoint)
        data = resp.json()
        if "membership" not in data:
            raise Exception("Invalid response: 'membership' key not found.")
        return data["membership"]
    except Exception as e:
        raise Exception(f"Failed to get project membership detail: {e}")
