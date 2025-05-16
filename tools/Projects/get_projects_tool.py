"""Redmine Project List Retrieval Tool

Retrieve a list of projects using RedmineAPIClient.
"""

from typing import Any, Dict, Optional

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
        redmine_url (str, optional): URL of the Redmine server. Uses environment variable REDMINE_URL if not specified.
        api_key (str, optional): Redmine API key. Uses environment variable REDMINE_ADMIN_API_KEY if not specified.
        include (str, optional): Additional information (comma-separated: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields)
        limit (int, optional): Number of items to retrieve
        offset (int, optional): Offset

    Returns:
        dict: Project list information
            - projects (list): List of project information
            - total_count (int): Total number of items
            - limit (int): Number of items retrieved
            - offset (int): Offset
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    resp = client.get("/projects.json", params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "projects": data.get("projects", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetProjectsTool = Tool.from_function(get_projects, name="get_projects", description="Get a list of Redmine projects")
