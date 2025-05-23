from typing import Any

import requests

from tools.redmine_api_client import RedmineAPIClient


def get_custom_fields(
    redmine_url: str,
    api_key: str,
) -> dict[str, Any]:
    """Get all custom fields definitions from Redmine.

    Args:
        redmine_url (str): Redmine server URL.
        api_key (str): Redmine admin API key.

    Returns:
        dict: Custom fields definitions.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    try:
        response = client.get(
            endpoint="/custom_fields.json",
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"custom_fields": []}
        raise
