import requests
from fastmcp.tools.tool import Tool


def get_versions(
    redmine_url: str,
    api_key: str,
    project_id: str = None,
    limit: int = None,
    offset: int = None,
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if project_id:
        url = f"{redmine_url.rstrip('/')}/projects/{project_id}/versions.json"
    else:
        url = f"{redmine_url.rstrip('/')}/versions.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "versions": data.get("versions", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetVersionTool = Tool.from_function(
    get_versions,
    name="get_versions",
    description="Get versions from Redmine",
)
