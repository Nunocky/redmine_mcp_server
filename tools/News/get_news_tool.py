import os
from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


def get_news(
    redmine_url: str,
    api_key: str,
    project_id: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
    """Get a list of news from Redmine.

    Args:
        redmine_url (str): The base URL of the Redmine instance.
        api_key (str): The API key for authentication.
        project_id (str, optional): Project ID or identifier (not used for all-projects news).
        limit (int, optional): Number of news to retrieve (pagination).
        offset (int, optional): Offset for pagination.

    Returns:
        dict: A dictionary containing news list, total_count, limit, and offset.

    Raises:
        ValueError: If required parameters are missing.
        Exception: When API request fails (excluding 404 errors)
    """
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_USER_API_KEY") or os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise ValueError("redmine_url and api_key are required.")

    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    if project_id:
        endpoint = f"/projects/{project_id}/news.json"
    else:
        endpoint = "/news.json"

    try:
        response = client.get(
            endpoint=endpoint,
            params=params,
        )
        data = response.json()
        # Ensure offset/limit are present in the result
        if "offset" not in data:
            data["offset"] = params.get("offset", 0)
        if "limit" not in data:
            data["limit"] = params.get("limit", 25)
        return data
    except Exception as e:
        # Raise exception for 404 errors (project not found)
        if hasattr(e, "response") and e.response is not None and getattr(e.response, "status_code", None) == 404:
            raise ValueError("指定された project_id は存在しません") from e
        raise
