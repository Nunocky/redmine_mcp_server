import os
from typing import Optional

import requests
from fastmcp.tools.tool import Tool


def get_news(
    redmine_url: str,
    api_key: str,
    project_id: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
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
        requests.RequestException: If the HTTP request fails.

    """
    # Use environment variables if parameters are not provided
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise ValueError("redmine_url and api_key are required.")

    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    url = f"{redmine_url.rstrip('/')}/news.json"

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        # Log the error or handle as needed
        raise requests.RequestException(f"Failed to fetch news from Redmine: {e}")

    return {
        "news": data.get("news", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetNewsTool = Tool.from_function(
    get_news,
    name="get_news",
    description="Get a list of news from Redmine.",
)
