"""Delete Issue Relation API function for Redmine.

This module provides a function to delete an issue relation in Redmine via its REST API.

"""

from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineApiClient


def delete_issue_relation(
    redmine_url: str,
    api_key: str,
    id: int,
    format: Optional[str] = "json",
) -> Dict[str, Any]:
    """Delete a relation by relation ID in Redmine.

    Args:
        redmine_url (str): Base URL of the Redmine server.
        api_key (str): Redmine API key.
        id (int): Relation ID to delete.
        format (Optional[str], optional): Response format ('json' or 'xml'). Defaults to 'json'.

    Returns:
        Dict[str, Any]: Empty dict if deleted, or API error response.

    Raises:
        ValueError: If the format is not 'json' or 'xml'.
        Exception: If the API request fails.

    """
    if format not in ("json", "xml"):
        raise ValueError("format must be 'json' or 'xml'")

    endpoint = f"{redmine_url}/relations/{id}.{format}"
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": f"application/{format}"}

    client = RedmineApiClient()
    response = client.delete(endpoint, headers=headers)
    # If deletion is successful, Redmine returns 204 No Content
    if hasattr(response, "status_code") and response.status_code == 204:
        return {}
    # If response is a dict with status_code
    if isinstance(response, dict) and response.get("status_code") == 204:
        return {}
    return response
