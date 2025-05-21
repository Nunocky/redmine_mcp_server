"""Tool class for retrieving Redmine TimeEntries list via REST API.

This tool fetches a list of time entries from Redmine using the REST API.

作業時間記録
"""

from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


def get_time_entries(
    redmine_url: str,
    api_key: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    user_id: Optional[int] = None,
    project_id: Optional[str] = None,
    spent_on: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Retrieve a list of Redmine TimeEntries using RedmineAPIClient."""
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if offset is not None:
        params["offset"] = offset
    if limit is not None:
        params["limit"] = limit
    if user_id is not None:
        params["user_id"] = user_id
    if project_id is not None:
        params["project_id"] = project_id
    if spent_on is not None:
        params["spent_on"] = spent_on
    if from_date is not None:
        params["from"] = from_date
    if to_date is not None:
        params["to"] = to_date

    try:
        resp = client.get("/time_entries.json", params=params)
        return resp.json()
    except Exception as e:
        status_code = getattr(e.response, "status_code", None) if hasattr(e, "response") else None
        response_text = getattr(e.response, "text", str(e)) if hasattr(e, "response") else str(e)
        return {"error": str(e), "status_code": status_code, "response": response_text}
