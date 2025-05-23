from typing import Any, Dict

import requests

from tools.redmine_api_client import RedmineAPIClient


def create_group(
    redmine_url: str,
    api_key: str,
    name: str,
    users: list = None,
    custom_fields: list = None,
) -> Dict[str, Any]:
    """Create a Redmine group.

    Args:
        redmine_url (str): Base URL of Redmine.
        api_key (str): Redmine API key.
        name (str): Group name.
        users (list, optional): List of user IDs to add to the group.
        custom_fields (list, optional): List of custom fields.

    Returns:
        dict: Created group information.

    Raises:
        Exception: When API request fails.
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    data = {"group": {"name": name}}
    if users is not None:
        data["group"]["user_ids"] = users
    if custom_fields is not None:
        data["group"]["custom_fields"] = custom_fields

    try:
        response = client.post(
            endpoint="/groups.json",
            json=data,
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise
