"""Create Issue Relation API function for Redmine.

This module provides a function to create an issue relation in Redmine via its REST API.

"""

from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


def create_issue_relation(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    issue_to_id: int,
    relation_type: str,
    delay: Optional[int] = None,
    format: Optional[str] = "json",
) -> Dict[str, Any]:
    """Create a new relation for a specific issue in Redmine.

    Args:
        redmine_url (str): Base URL of the Redmine server.
        api_key (str): Redmine API key.
        issue_id (int): Source issue ID.
        issue_to_id (int): Target issue ID.
        relation_type (str): Relation type (e.g., relates, blocks, precedes).
        delay (Optional[int], optional): Delay days (for precedes, etc.). Defaults to None.
        format (Optional[str], optional): Response format ('json' or 'xml'). Defaults to 'json'.

    Returns:
        Dict[str, Any]: API response as a dictionary.

    Raises:
        ValueError: If the format is not 'json' or 'xml'.
        Exception: If the API request fails.

    """
    if format not in ("json", "xml"):
        raise ValueError("format must be 'json' or 'xml'")

    endpoint = f"/issues/{issue_id}/relations.{format}"
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": f"application/{format}"}

    relation_data = {"issue_to_id": issue_to_id, "relation_type": relation_type}
    if delay is not None:
        relation_data["delay"] = delay

    body = {"relation": relation_data}

    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    response = client.post(endpoint, json=body, headers=headers)
    return response
