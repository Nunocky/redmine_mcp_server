"""GetRoleTool: Fetch the detail of a specific role from Redmine.

This module provides a function and a Tool object to retrieve a specific role's detail from the Redmine REST API.
"""

from fastmcp.tools.tool import Tool
from tools.redmine_api_client import RedmineAPIClient
from typing import Any, Dict, Optional


def get_role(
    role_id: int,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Fetch the detail of a specific role from Redmine.

    Args:
        role_id (int): Role ID to fetch.
        redmine_url: URL of the Redmine server
        api_key: Redmine API key

    Returns:
        dict: Dictionary containing the role detail.

    Raises:
        Exception: If the API request fails or returns an error.
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    response = client.get(f"/roles/{role_id}.json")
    if not response.ok:
        raise Exception(f"Failed to fetch role: {response.status_code} {response.text}")
    data = response.json()
    return {"role": data.get("role", {})}


GetRoleTool = Tool.from_function(
    get_role,
    name="get_role",
    description="Get the detail of a specific role from Redmine.",
)
