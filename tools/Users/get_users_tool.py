"""Redmine User List Retrieval Tool

Retrieves a list of users using RedmineAPIClient.
"""

from typing import Any, Dict, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


async def get_users(
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
        redmine_url (str, optional): Redmine server URL. If not specified, the REDMINE_URL environment variable is used.
        api_key (str, optional): Redmine API key. If not specified, the REDMINE_ADMIN_API_KEY environment variable is used.
        limit (int, optional): Number of records to retrieve.
        offset (int, optional): Number of records to skip.
        status (int, optional): User status (1: active, 2: registered, 3: locked).
        name (str, optional): Filter by login, name, or email address.
        group_id (int, optional): Filter users belonging to the specified group.

    Returns:
        dict: User list information
            - users (list): List of user information
            - total_count (int): Total number of users
            - limit (int): Number of records retrieved
            - offset (int): Offset
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
    resp = client.get("/users.json", params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "users": data.get("users", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetUsersTool = Tool.from_function(
    get_users,
    name="get_users",
    description="Retrieve a list of users from Redmine.",
)
