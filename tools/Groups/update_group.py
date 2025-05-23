import requests
from tools.redmine_api_client import RedmineAPIClient


def update_group(
    redmine_url: str,
    api_key: str,
    group_id: int,
    name: str = None,
    users: list = None,
    custom_fields: list = None,
):
    """Update a Redmine group.

    Args:
        redmine_url (str): Base URL of Redmine.
        api_key (str): Redmine API key.
        group_id (int): Group ID.
        name (str, optional): Group name.
        users (list, optional): List of user IDs.
        custom_fields (list, optional): List of custom fields.

    Returns:
        dict: Updated group information. Returns {"group": None} for 404.

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    data = {"group": {}}
    if name is not None:
        data["group"]["name"] = name
    if users is not None:
        data["group"]["user_ids"] = users
    if custom_fields is not None:
        data["group"]["custom_fields"] = custom_fields

    try:
        response = client.put(
            endpoint=f"/groups/{group_id}.json",
            json=data,
        )
        # RedmineのPUT /groups/{id}.jsonは204 No Contentを返す場合がある
        if response.status_code == 204:
            return {"group": None}
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"group": None}
        raise
