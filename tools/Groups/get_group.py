import requests

from tools.redmine_api_client import RedmineAPIClient


def get_group(
    redmine_url: str,
    api_key: str,
    group_id: int,
):
    """Get Redmine group detail.

    Args:
        redmine_url (str): Base URL of Redmine.
        api_key (str): Redmine API key.
        group_id (int): Group ID.

    Returns:
        dict: Group detail information. Returns {"group": None} for 404.

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    try:
        response = client.get(
            endpoint=f"/groups/{group_id}.json",
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"group": None}
        raise
