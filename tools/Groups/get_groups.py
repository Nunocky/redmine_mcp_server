import requests
from tools.redmine_api_client import RedmineAPIClient


def get_groups(
    redmine_url: str,
    api_key: str,
    limit: int = None,
    offset: int = None,
    name: str = None,
):
    """Get Redmine groups list.

    Args:
        redmine_url (str): Base URL of Redmine.
        api_key (str): Redmine API key.
        limit (int, optional): Number of records to retrieve.
        offset (int, optional): Number of records to skip.
        name (str, optional): Filter by group name.

    Returns:
        dict: Groups list and page information. Returns empty list for 404.

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if name is not None:
        params["name"] = name

    try:
        response = client.get(
            endpoint="/groups.json",
            params=params,
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"groups": []}
        raise
