"""Redmine User Details Retrieval Tool

Retrieve user details using RedmineAPIClient.
Returns the API response as-is (including or not including the 'user' key).
Raises Exception on 404 or other HTTP errors.

Returns:
    dict: The API response as-is

Raises:
    Exception: When the API request fails (including 404 errors)
"""

from typing import Any, Dict, Optional, Union

from tools.redmine_api_client import RedmineAPIClient


def get_user(
    redmine_url: str,
    api_key: str,
    user_id: Union[int, str],
    include: Optional[str] = None,
) -> Dict[str, Any]:
    """Get Redmine user details

    Args:
        redmine_url: Redmine URL
        api_key: Redmine API key
        user_id: User ID or 'current' (current user)
        include: Related information to include in the response (memberships, groups)

    Returns:
        The API response as-is

    Raises:
        Exception: When the API request fails (including 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    endpoint = f"/users/{user_id}.json"
    resp = client.get(endpoint, params=params)
    resp.raise_for_status()
    return resp.json()
