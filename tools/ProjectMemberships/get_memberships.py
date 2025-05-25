"""Redmineのプロジェクトメンバーシップ一覧取得API呼び出し関数

存在しないリソース（404エラー）は空リストを返す。

Returns:
    dict: Membership list and page information

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests

from tools.redmine_api_client import RedmineAPIClient


def get_memberships(
    redmine_url: str,
    api_key: str,
    project_id: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Get the list of Redmine project memberships

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        project_id: Project ID or identifier
        offset: Number of records to skip
        limit: Number of records to retrieve

    Returns:
        dict: List of memberships and page information
        Returns an empty list if the resource does not exist (404 error)

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    endpoint = f"/projects/{project_id}/memberships.json"
    try:
        response = client.get(
            endpoint=endpoint,
            params=params,
        )
        data = response.json()
        if "offset" not in data:
            data["offset"] = params.get("offset", 0)
        if "limit" not in data:
            data["limit"] = params.get("limit", 25)
        return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"memberships": [], "total_count": 0, "offset": 0, "limit": 0}
        raise
