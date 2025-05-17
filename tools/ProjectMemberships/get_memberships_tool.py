"""Redmine Project Membership List Retrieval Tool

This tool retrieves a list of project memberships from Redmine.
"""

from typing import Any, Dict, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_memberships(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    """Get a list of project memberships

    Args:
        redmine_url (str): URL of the Redmine server
        api_key (str): Redmine API key
        project_id (str): Project ID
        limit (int, optional): Number of items to retrieve
        offset (int, optional): Number of items to skip

    Returns:
        dict: List of memberships and page information

    Raises:
        Exception: When API request fails
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    endpoint = f"/projects/{project_id}/memberships.json"
    response = client.get(
        endpoint=endpoint,
        params=params,
    )
    data = response.json()
    return {
        "memberships": data.get("memberships", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetMembershipsTool = Tool.from_function(
    get_memberships,
    name="get_projects",
    description="Get a list of Redmine project memberships",
)
