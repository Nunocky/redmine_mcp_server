"""Update Issue Tool

This tool updates an existing Redmine issue.
Returns an empty dict for non-existent resources (404 error).

Returns:
    dict: API response or {"success": True} for 204 No Content

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def update_issue(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    subject: Optional[str] = None,
    description: Optional[str] = None,
    tracker_id: Optional[int] = None,
    status_id: Optional[int] = None,
    priority_id: Optional[int] = None,
    category_id: Optional[int] = None,
    fixed_version_id: Optional[int] = None,
    assigned_to_id: Optional[int] = None,
    parent_issue_id: Optional[int] = None,
    custom_fields: Optional[Any] = None,
    watcher_user_ids: Optional[Any] = None,
    is_private: Optional[bool] = None,
    estimated_hours: Optional[float] = None,
    notes: Optional[str] = None,
    private_notes: Optional[bool] = None,
    uploads: Optional[Any] = None,
) -> Dict[str, Any]:
    """Update an existing Redmine issue

    Args:
        redmine_url: Redmine base URL
        api_key: Redmine API key
        issue_id: Issue ID to update
        subject: Issue subject
        description: Issue description
        tracker_id: Tracker ID
        status_id: Status ID
        priority_id: Priority ID
        category_id: Category ID
        fixed_version_id: Fixed version ID
        assigned_to_id: Assigned user ID
        parent_issue_id: Parent issue ID
        custom_fields: Custom fields
        watcher_user_ids: Watcher user IDs
        is_private: Private issue flag
        estimated_hours: Estimated hours
        notes: Update notes
        private_notes: Private notes flag
        uploads: Attachments

    Returns:
        API response as dict, or {"success": True} for 204 No Content.
        Returns empty dict for non-existent resources (404 error).

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    issue_data: Dict[str, Any] = {}
    if subject is not None:
        issue_data["subject"] = subject
    if description is not None:
        issue_data["description"] = description
    if tracker_id is not None:
        issue_data["tracker_id"] = tracker_id
    if status_id is not None:
        issue_data["status_id"] = status_id
    if priority_id is not None:
        issue_data["priority_id"] = priority_id
    if category_id is not None:
        issue_data["category_id"] = category_id
    if fixed_version_id is not None:
        issue_data["fixed_version_id"] = fixed_version_id
    if assigned_to_id is not None:
        issue_data["assigned_to_id"] = assigned_to_id
    if parent_issue_id is not None:
        issue_data["parent_issue_id"] = parent_issue_id
    if custom_fields is not None:
        issue_data["custom_fields"] = custom_fields
    if watcher_user_ids is not None:
        issue_data["watcher_user_ids"] = watcher_user_ids
    if is_private is not None:
        issue_data["is_private"] = is_private
    if estimated_hours is not None:
        issue_data["estimated_hours"] = estimated_hours
    if uploads is not None:
        issue_data["uploads"] = uploads
    if notes is not None:
        issue_data["notes"] = notes
    if private_notes is not None:
        issue_data["private_notes"] = private_notes

    try:
        response = client.put(
            endpoint=f"/issues/{issue_id}.json",
            json={"issue": issue_data},
        )
        if response.status_code == 204:
            return {"success": True}
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {}
        raise


UpdateIssueTool = Tool.from_function(
    update_issue,
    name="update_issue",
    description="Update an existing issue in Redmine.",
)
