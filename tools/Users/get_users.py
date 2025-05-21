"""Redmine User List Retrieval Tool

Retrieves a list of users using RedmineAPIClient.
404エラー時は空dict、他エラーは例外送出。

Returns:
    dict: User list information or {} for 404

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_users(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    status: Optional[int] = None,
    name: Optional[str] = None,
    group_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Retrieve a list of Redmine users.

    Args:
        redmine_url: Redmine server URL.
        api_key: Redmine API key.
        limit: Number of records to retrieve.
        offset: Number of records to skip.
        status: User status (1: active, 2: registered, 3: locked).
        name: Filter by login, name, or email address.
        group_id: Filter users belonging to the specified group.

    Returns:
        User list information as dict, or {} for 404

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if status is not None:
        params["status"] = status
    if name is not None:
        params["name"] = name
    if group_id is not None:
        params["group_id"] = group_id
    try:
        resp = client.get("/users.json", params=params)
        data = resp.json()
        return {
            "users": data.get("users", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {}
        raise


GetUsersTool = Tool.from_function(
    get_users,
    name="get_users",
    description="Retrieve a list of users from Redmine.",
)
