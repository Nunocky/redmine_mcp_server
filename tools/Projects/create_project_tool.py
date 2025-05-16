"""Redmine Project Creation Tool

Create a new project using RedmineAPIClient.
"""

from typing import Any, Dict, List, Optional

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
        name (str): Project name (required)
        identifier (str): Project identifier (required)
        redmine_url (str, optional): URL of the Redmine server
        api_key (str, optional): Redmine API key
        description (str, optional): Description
        homepage (str, optional): Homepage URL
        is_public (bool, optional): Public flag
        parent_id (int, optional): Parent project ID
        inherit_members (bool, optional): Inherit members
        default_assigned_to_id (int, optional): Default assignee ID
        default_version_id (int, optional): Default version ID
        tracker_ids (List[int], optional): List of tracker IDs
        enabled_module_names (List[str], optional): List of enabled module names
        issue_custom_field_ids (List[int], optional): List of custom field IDs
        custom_field_values (Dict[str, Any], optional): Custom field values

    Returns:
        dict: Information of the created project or error message
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
    resp = client.post("/projects.json", json=payload)
    resp.raise_for_status()
    return resp.json().get("project", {})


CreateProjectTool = Tool.from_function(create_project, name="create_project", description="Create a Redmine project")
