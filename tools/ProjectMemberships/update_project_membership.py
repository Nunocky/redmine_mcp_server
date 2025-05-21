import os
from typing import Any, Dict, List, Optional

from tools.ProjectMemberships.get_project_membership import get_project_membership
from tools.redmine_api_client import RedmineAPIClient


def update_project_membership(
    membership_id: int,
    role_ids: List[int],
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Update the roles of a project membership in Redmine.

    Args:
        membership_id (int): Membership ID to update.
        role_ids (List[int]): List of role IDs to assign.
        redmine_url (str, optional): The base URL of the Redmine instance.
        api_key (str, optional): The API key for authentication.

    Returns:
        dict: Updated membership information.

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
    payload = {"membership": {"role_ids": role_ids}}
    try:
        resp = client.put(endpoint, json=payload)
        if resp.status_code == 204:
            # Retrieve latest membership info after update
            return get_project_membership(membership_id, redmine_url=redmine_url, api_key=api_key)
        data = resp.json()
        if "membership" not in data:
            raise Exception(f"Invalid API response: 'membership' key not found. Response content: {data}")
        return data["membership"]
    except Exception as e:
        raise Exception(f"Failed to update project membership (ID: {membership_id}, roles: {role_ids}): {e}")
