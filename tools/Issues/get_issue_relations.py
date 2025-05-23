"""Get Issue Relations API function for Redmine.

This module provides a function to retrieve issue relations from Redmine via its REST API.

"""

from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineApiClient


def get_issue_relations(redmine_url: str, api_key: str, issue_id: int, format: Optional[str] = "json") -> Dict[str, Any]:
    """Retrieve relations for a specific issue from Redmine.

    Args:
        redmine_url (str): Base URL of the Redmine server.
        api_key (str): Redmine API key.
        issue_id (int): Target issue ID.
        format (Optional[str], optional): Response format ('json' or 'xml'). Defaults to 'json'.

    Returns:
        Dict[str, Any]: API response as a dictionary.

    Raises:
        ValueError: If the format is not 'json' or 'xml'.
        Exception: If the API request fails.

    """
    if format not in ("json", "xml"):
        raise ValueError("format must be 'json' or 'xml'")

    endpoint = f"{redmine_url}/issues/{issue_id}/relations.{format}"
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": f"application/{format}"}

    client = RedmineApiClient()
    response = client.get(endpoint, headers=headers)
    return response
