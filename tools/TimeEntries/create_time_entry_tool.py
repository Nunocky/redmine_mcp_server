import requests
from fastmcp.tools.tool import Tool


def create_time_entry(
    redmine_url: str,
    api_key: str,
    issue_id: int = None,
    project_id: str = None,
    spent_on: str = None,
    hours: float = None,
    activity_id: int = None,
    comments: str = None,
    user_id: int = None,
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
    time_entry_data = {}
    if issue_id is not None:
        time_entry_data["issue_id"] = issue_id
    if project_id is not None:
        time_entry_data["project_id"] = project_id
    if spent_on is not None:
        time_entry_data["spent_on"] = spent_on
    if hours is not None:
        time_entry_data["hours"] = hours
    if activity_id is not None:
        time_entry_data["activity_id"] = activity_id
    if comments is not None:
        time_entry_data["comments"] = comments
    if user_id is not None:
        time_entry_data["user_id"] = user_id

    url = f"{redmine_url.rstrip('/')}/time_entries.json"
    resp = requests.post(url, headers=headers, json={"time_entry": time_entry_data})
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        # Also return the response body
        return {"error": str(e), "status_code": resp.status_code, "response": resp.text}
    return {"time_entry": resp.json().get("time_entry", {})}


CreateTimeEntryTool = Tool.from_function(
    create_time_entry, name="create_time_entry", description="Create a new time entry in Redmine."
)
