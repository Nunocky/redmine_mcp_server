from typing import Optional, Union

import requests
from fastmcp.tools.tool import Tool


def get_user(
    redmine_url: str,
    api_key: str,
    user_id: Union[int, str],
    include: Optional[str] = None,
):
    """Get Redmine user details

    Args:
        redmine_url (str): Redmine URL
        api_key (str): Redmine API key
        user_id (Union[int, str]): User ID or 'current' (current user)
        include (Optional[str], optional): Related information to include in the response (memberships, groups)

    Returns:
        Dict[str, Any]: User details information

    Raises:
        requests.exceptions.HTTPError: When API request fails
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if include:
        params["include"] = include
    url = f"{redmine_url.rstrip('/')}/users/{user_id}.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()


GetUserTool = Tool.from_function(
    get_user,
    name="get_user",
    description="Get Redmine user details",
)
