import os
from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


def delete_project_membership(
    membership_id: int,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a project membership by ID.

    Args:
        membership_id (int): The ID of the membership to delete.
        redmine_url (str, optional): The base URL of the Redmine instance.
        api_key (str, optional): The API key for authentication.

    Returns:
        dict: Result with status code or error message.

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
        resp = client.delete(endpoint)
        if resp.status_code == 204:
            return {"status": "success", "status_code": 204}
        return {"status": "failed", "status_code": resp.status_code, "message": resp.text}
    except Exception as e:
        if hasattr(e, "response") and hasattr(e.response, "status_code"):
            return {"status": "failed", "status_code": e.response.status_code, "message": str(e)}
        return {"status": "failed", "status_code": None, "message": str(e)}
