"""Redmine Project Creation Tool

Create a new project using RedmineAPIClient.
Returns an empty dict for non-existent resources (404 error).

Returns:
    dict: Created project information

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, List, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def create_project(
    name: str,
    identifier: str,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    description: Optional[str] = None,
    homepage: Optional[str] = None,
    is_public: Optional[bool] = None,
    parent_id: Optional[int] = None,
    inherit_members: Optional[bool] = None,
    default_assigned_to_id: Optional[int] = None,
    default_version_id: Optional[int] = None,
    tracker_ids: Optional[List[int]] = None,
    enabled_module_names: Optional[List[str]] = None,
    issue_custom_field_ids: Optional[List[int]] = None,
    custom_field_values: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a new Redmine project

    Args:
        name: Project name (required)
        identifier: Project identifier (required)
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        description: Description
        homepage: Homepage URL
        is_public: Public flag
        parent_id: Parent project ID
        inherit_members: Inherit members
        default_assigned_to_id: Default assignee ID
        default_version_id: Default version ID
        tracker_ids: List of tracker IDs
        enabled_module_names: List of enabled module names
        issue_custom_field_ids: List of custom field IDs
        custom_field_values: Custom field values

    Returns:
        Created project information as dict.
        Returns empty dict for non-existent resources (404 error).

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    project_data = {
        "name": name,
        "identifier": identifier,
    }
    if description is not None:
        project_data["description"] = description
    if homepage is not None:
        project_data["homepage"] = homepage
    if is_public is not None:
        project_data["is_public"] = is_public
    if parent_id is not None:
        project_data["parent_id"] = parent_id
    if inherit_members is not None:
        project_data["inherit_members"] = inherit_members
    if default_assigned_to_id is not None:
        project_data["default_assigned_to_id"] = default_assigned_to_id
    if default_version_id is not None:
        project_data["default_version_id"] = default_version_id
    if tracker_ids is not None:
        project_data["tracker_ids"] = tracker_ids
    if enabled_module_names is not None:
        project_data["enabled_module_names"] = enabled_module_names
    if issue_custom_field_ids is not None:
        project_data["issue_custom_field_ids"] = issue_custom_field_ids
    if custom_field_values is not None:
        project_data["custom_field_values"] = custom_field_values

    payload = {"project": project_data}
    try:
        resp = client.post(
            "/projects.json",
            json=payload,
        )
        return resp.json().get("project", {})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {}
        raise


CreateProjectTool = Tool.from_function(
    create_project,
    name="create_project",
    description="Create a Redmine project",
)
