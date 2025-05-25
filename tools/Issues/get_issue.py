"""Redmine Issue Details Retrieval Tool"""

from typing import Any, Dict

import requests

from tools.redmine_api_client import RedmineAPIClient


def get_issue(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    include: str = None,
) -> Dict[str, Any]:
    """Get detailed information for the specified issue (issue_id)

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        issue_id (int): Issue ID
        include (str, optional): Additional information (comma-separated)

    Returns:
        dict: Issue details information
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    params = {}
    if include:
        params["include"] = include

    try:
        response = client.get(
            endpoint=f"/issues/{issue_id}.json",
            params=params,
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"issue": None}
        raise
