"""Get all trackers from Redmine via REST API.

Returns a list of tracker dicts.
"""

from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_trackers(
    redmine_url: str,
    api_key: str,
) -> Dict[str, Any]:
    """Get all trackers from Redmine.

    Args:
        redmine_url (str): Base URL of Redmine (e.g. https://redmine.example.com)
        api_key (str): Redmine API key

    Returns:
        list[dict]: List of tracker dicts. Each dict contains:
            - id (int)
            - name (str)
            - default_status (dict: id, name)
            - description (str, nullable)
            - enabled_standard_fields (list[str], optional, Redmine 5.0+)
    Raises:
        Exception: If the API request fails or response is invalid
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    response = client.get("/trackers.json").json()
    if "trackers" not in response:
        raise Exception("Invalid response: 'trackers' key not found")
    return response["trackers"]
