"""Redmine Project Details Retrieval Tool

Retrieve project details using RedmineAPIClient.
"""

from typing import Any, Dict, Optional

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
        project_id_or_identifier (str): Project ID or identifier
        redmine_url (str, optional): URL of the Redmine server. Uses environment variable REDMINE_URL if not specified.
        api_key (str, optional): Redmine API key. Uses environment variable REDMINE_ADMIN_API_KEY if not specified.
        include (str, optional): Additional information (comma-separated: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields)

    Returns:
        dict: Project details information
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    endpoint = f"/projects/{project_id_or_identifier}.json"
    resp = client.get(endpoint, params=params)
    resp.raise_for_status()
    return resp.json().get("project", {})


GetProjectTool = Tool.from_function(get_project, name="get_project", description="Get Redmine project information")
