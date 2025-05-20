"""GetRolesTool: Fetch the list of roles from Redmine.

This module provides a function and a Tool object to retrieve all roles from the Redmine REST API.
"""

from typing import Any, Dict, List, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_roles(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch the list of roles from Redmine.

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key

    Returns:
        dict: Dictionary containing the list of roles.

    Raises:
        Exception: If the API request fails or returns an error.
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    response = client.get("/roles.json")
    if not response.ok:
        raise Exception(f"Failed to fetch roles: {response.status_code} {response.text}")
    data = response.json()
    return {"roles": data.get("roles", [])}


GetRolesTool = Tool.from_function(
    get_roles,
    name="get_roles",
    description="Get the list of roles from Redmine.",
)
