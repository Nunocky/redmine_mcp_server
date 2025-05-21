"""Redmine Project List Retrieval Tool

Retrieve a list of projects using RedmineAPIClient.
404エラー時は空dict、他エラーは例外送出。

Returns:
    dict: Project list information or {} for 404

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_projects(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    include: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    """Get a list of Redmine projects

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        include: Additional information (comma-separated: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields)
        limit: Number of items to retrieve
        offset: Offset

    Returns:
        Project list information as dict, or {} for 404

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    try:
        resp = client.get("/projects.json", params=params)
        data = resp.json()
        return {
            "projects": data.get("projects", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {}
        raise


GetProjectsTool = Tool.from_function(
    get_projects,
    name="get_projects",
    description="Get a list of Redmine projects",
)
