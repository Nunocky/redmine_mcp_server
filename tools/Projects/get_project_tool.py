"""Redmine Project Details Retrieval Tool

Retrieve project details using RedmineAPIClient.
404エラー時は空dict、他エラーは例外送出。

Returns:
    dict: Project details information or {} for 404

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_project(
    redmine_url: str,
    api_key: str,
    project_id_or_identifier: str,
    include: Optional[str] = None,
) -> Dict[str, Any]:
    """Get Redmine project details

    Args:
        project_id_or_identifier: Project ID or identifier
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        include: Additional information (comma-separated: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields)

    Returns:
        Project details information as dict, or {} for 404

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    endpoint = f"/projects/{project_id_or_identifier}.json"
    try:
        resp = client.get(endpoint, params=params)
        return resp.json().get("project", {})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {}
        raise


GetProjectTool = Tool.from_function(
    get_project,
    name="get_project",
    description="Get Redmine project information",
)
