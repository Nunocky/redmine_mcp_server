"""Issue List Retrieval Tool

This tool retrieves a list of Redmine issues.
Returns an empty result for non-existent resources (404 error).

Returns:
    dict: Issue list and page information

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_issues(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    include: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Get a list of Redmine issues

    Args:
        offset: Number of items to skip
        limit: Number of items to retrieve
        sort: Sort column (e.g., 'updated_on:desc')
        include: Additional information (comma-separated)
        filters: Other filter conditions

    Returns:
        Issue list and page information
        Returns an empty result for non-existent resources (404 error)

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    # Call the API directly using RedmineAPIClient
    client = RedmineAPIClient()
    params: Dict[str, Any] = {}
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if sort is not None:
        params["sort"] = sort
    if include is not None:
        params["include"] = include
    if filters:
        params.update(filters)

    try:
        response = client.get(
            endpoint="/issues.json",
            params=params,
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Return an empty result for 404 errors
        if e.response.status_code == 404:
            return {"issues": [], "total_count": 0, "offset": 0, "limit": 0}
        # Re-raise other errors
        raise


GetIssuesTool = Tool.from_function(
    get_issues,
    name="get_issues",
    description="Get a list of Redmine issues",
)
