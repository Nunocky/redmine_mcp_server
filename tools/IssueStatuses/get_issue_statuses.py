"""Get issue statuses from Redmine via REST API.

This module provides a function to retrieve all issue statuses from Redmine.
"""

from typing import Any, Dict, List

import requests


def get_issue_statuses(redmine_url: str, api_key: str) -> List[Dict[str, Any]]:
    """Retrieve all issue statuses from Redmine.

    Args:
        redmine_url (str): Base URL of the Redmine server (e.g., https://redmine.example.com).
        api_key (str): Redmine API key.

    Returns:
        List[Dict[str, Any]]: List of issue status dicts with keys 'id', 'name', 'is_closed'.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = f"{redmine_url.rstrip('/')}/issue_statuses.json"
    headers = {"X-Redmine-API-Key": api_key}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("issue_statuses", [])
