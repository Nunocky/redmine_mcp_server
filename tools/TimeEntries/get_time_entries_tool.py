import requests
from fastmcp.tools.tool import Tool


def get_time_entries(
    redmine_url: str, api_key: str, project_id: str = None, user_id: int = None, limit: int = None, offset: int = None
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if project_id:
        params["project_id"] = project_id
    if user_id is not None:
        params["user_id"] = user_id
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    url = f"{redmine_url.rstrip('/')}/time_entries.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "time_entries": data.get("time_entries", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetTimeEntriesTool = Tool.from_function(
    get_time_entries, name="get_time_entries", description="Get a list of time entries from Redmine."
)
