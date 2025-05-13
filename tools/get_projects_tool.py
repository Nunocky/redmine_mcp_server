import requests
from fastmcp.tools.tool import Tool


def get_projects(redmine_url: str, api_key: str, limit: int = None, offset: int = None):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    url = f"{redmine_url.rstrip('/')}/projects.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "projects": data.get("projects", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetProjectsTool = Tool.from_function(get_projects, name="get_projects", description="Get a list of projects from Redmine.")
