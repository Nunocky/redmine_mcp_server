"""Redmine User Details Retrieval Tool

Get user details using RedmineAPIClient.
APIレスポンスをそのまま返却（userキー含む場合も含まない場合も）。
404や他HTTPエラー時はException送出。

Returns:
    dict: APIレスポンスそのまま

Raises:
    Exception: When API request fails (including 404 errors)
"""

from typing import Any, Dict, Optional, Union

from tools.redmine_api_client import RedmineAPIClient


def get_user(
    redmine_url: str,
    api_key: str,
    user_id: Union[int, str],
    include: Optional[str] = None,
) -> Dict[str, Any]:
    """Get Redmine user details

    Args:
        redmine_url: Redmine URL
        api_key: Redmine API key
        user_id: User ID or 'current' (current user)
        include: Related information to include in the response (memberships, groups)

    Returns:
        APIレスポンスそのまま

    Raises:
        Exception: When API request fails (including 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    endpoint = f"/users/{user_id}.json"
    resp = client.get(endpoint, params=params)
    resp.raise_for_status()
    return resp.json()
