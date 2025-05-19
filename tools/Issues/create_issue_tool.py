"""Redmine Issue Creation Tool

This tool creates a new Redmine issue.
"""

import os
from typing import Any, Dict, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def create_issue(
    redmine_url: str,
    api_key: str,
    project_id: str,
    subject: str,
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
    uploads: Optional[Any] = None,
) -> Dict[str, Any]:
    """Create a new issue in Redmine.

    Args:
        redmine_url (str): The base URL of the Redmine instance.
        api_key (str): The API key for authentication.
        project_id (str): Project ID
        subject (str): Subject
        description (str, optional): Description
        tracker_id (int, optional): Tracker ID
        status_id (int, optional): Status ID
        priority_id (int, optional): Priority ID
        category_id (int, optional): Category ID
        fixed_version_id (int, optional): Version ID
        assigned_to_id (int, optional): Assignee ID
        parent_issue_id (int, optional): Parent issue ID
        custom_fields (Any, optional): Custom fields
        watcher_user_ids (Any, optional): List of watcher IDs
        is_private (bool, optional): Private flag
        estimated_hours (float, optional): Estimated hours
        uploads (Any, optional): Attached files

    Returns:
        dict: Information of the created issue

    Raises:
        ValueError: If required parameters are missing.
        Exception: When API request fails
    """
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_USER_API_KEY") or os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise ValueError("redmine_url and api_key are required.")

    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    issue_data: Dict[str, Any] = {
        "project_id": project_id,
        "subject": subject,
    }
    if description:
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
    if custom_fields:
        issue_data["custom_fields"] = custom_fields
    if watcher_user_ids:
        issue_data["watcher_user_ids"] = watcher_user_ids
    if is_private is not None:
        issue_data["is_private"] = is_private
    if estimated_hours is not None:
        issue_data["estimated_hours"] = estimated_hours
    if uploads:
        issue_data["uploads"] = uploads

    response = client.post(
        endpoint="/issues.json",
        json={"issue": issue_data},
    )
    issue = response.json().get("issue")
    # 添付ファイル情報を取得するため再取得
    if issue and "id" in issue:
        issue_id = issue["id"]
        try:
            detail_resp = client.get(f"/issues/{issue_id}.json", params={"include": "attachments"})
            detail_json = detail_resp.json()
            if "issue" in detail_json:
                return detail_json
        except Exception:
            pass
    return response.json()


CreateIssueTool = Tool.from_function(
    create_issue,
    name="create_issue",
    description="Create a new issue in Redmine.",
)
