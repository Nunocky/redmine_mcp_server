from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


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
) -> Dict[str, Any]:
    """Create a new time entry in Redmine using RedmineAPIClient."""
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
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

    try:
        resp = client.post("/time_entries.json", json={"time_entry": time_entry_data})
        return {"time_entry": resp.json().get("time_entry", {})}
    except Exception as e:
        # 失敗時はエラー内容・status_code・レスポンスボディを返す
        status_code = getattr(e.response, "status_code", None) if hasattr(e, "response") else None
        response_text = getattr(e.response, "text", str(e)) if hasattr(e, "response") else str(e)
        return {"error": str(e), "status_code": status_code, "response": response_text}
