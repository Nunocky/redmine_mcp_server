import requests
from fastmcp.tools.tool import Tool


def update_issue(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    subject: str = None,
    description: str = None,
    tracker_id: int = None,
    status_id: int = None,
    priority_id: int = None,
    category_id: int = None,
    fixed_version_id: int = None,
    assigned_to_id: int = None,
    parent_issue_id: int = None,
    custom_fields=None,
    watcher_user_ids=None,
    is_private: bool = None,
    estimated_hours: float = None,
    notes: str = None,
    private_notes: bool = None,
    uploads=None,
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
    issue_data = {}
    if subject:
        issue_data["subject"] = subject
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
    if notes is not None:
        issue_data["notes"] = notes
    if private_notes is not None:
        issue_data["private_notes"] = private_notes
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
    resp = requests.put(url, headers=headers, json={"issue": issue_data})
    return {
        "success": resp.status_code in (200, 204),
        "status_code": resp.status_code,
        "response_text": resp.text,
    }


UpdateIssueTool = Tool.from_function(
    update_issue,
    name="update_issue",
    description="Update an existing issue in Redmine.",
)
