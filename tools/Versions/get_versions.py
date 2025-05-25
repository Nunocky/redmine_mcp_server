"""
Get the list of Redmine project versions.
"""
from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_versions(
    redmine_url: str,
    api_key: str,
    project_id: str = None,
    limit: int = None,
    offset: int = None,
) -> Dict[str, Any]:
    """Get the list of Redmine project versions.

    Args:
        redmine_url (str): URL of the Redmine server.
        api_key (str): Redmine API key.
        project_id (str, optional): Project ID or identifier. If None, retrieves all versions.
        limit (int, optional): Number of records to retrieve. Defaults to 25 if not specified.
        offset (int, optional): Number of records to skip. Defaults to 0 if not specified.
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if project_id:
        endpoint = f"/projects/{project_id}/versions.json"
    else:
        endpoint = "/versions.json"
    try:
        response = client.get(endpoint=endpoint, params=params)
        data = response.json()
        return {
            "versions": data.get("versions", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
    except Exception as e:
        if hasattr(e, "response") and e.response is not None and getattr(e.response, "status_code", None) == 404:
            return {"versions": [], "total_count": 0, "limit": 0, "offset": 0}
        raise
