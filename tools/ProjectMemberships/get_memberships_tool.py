"""Project Membership List Retrieval Tool

This tool retrieves a list of project memberships from Redmine.
Returns an empty result for non-existent resources (404 error).

Returns:
    dict: Membership list and page information

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_memberships(
    redmine_url: str,
    api_key: str,
    project_id: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    """Get a list of project memberships

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        project_id: Project ID or identifier
        limit: Number of items to retrieve
        offset: Number of items to skip

    Returns:
        Membership list and page information
        Returns an empty result for non-existent resources (404 error)

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    # Create Redmine API client
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    endpoint = f"/projects/{project_id}/memberships.json"
    try:
        response = client.get(
            endpoint=endpoint,
            params=params,
        )
        data = response.json()
        # Ensure offset/limit are present in the result
        if "offset" not in data:
            data["offset"] = params.get("offset", 0)
        if "limit" not in data:
            data["limit"] = params.get("limit", 25)
        return {
            "memberships": data.get("memberships", []),
            "total_count": data.get("total_count", 0),
            "limit": data["limit"],
            "offset": data["offset"],
        }
    except requests.exceptions.HTTPError as e:
        # Return an empty result for 404 errors
        if e.response.status_code == 404:
            return {"memberships": [], "total_count": 0, "offset": 0, "limit": 0}
        # Re-raise other errors
        raise


GetMembershipsTool = Tool.from_function(
    get_memberships,
    name="get_memberships",
    description="Get a list of Redmine project memberships",
)
