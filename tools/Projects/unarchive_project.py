"""Project Unarchive Tool

This tool unarchives a Redmine project.
Returns an empty result for non-existent resources (404 error).

Returns:
    dict: Unarchive result (status, message)

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict

import requests

from tools.redmine_api_client import RedmineAPIClient


def unarchive_project(
    redmine_url: str,
    api_key: str,
    project_id_or_identifier: str,
) -> Dict[str, Any]:
    """Unarchive a Redmine project

    Args:
        redmine_url (str): URL of the Redmine server
        api_key (str): Redmine API key
        project_id_or_identifier (str): Project ID or identifier

    Returns:
        dict: Unarchive result (status, message)
        Returns an empty result for non-existent resources (404 error)

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    try:
        response = client.put(
            endpoint=f"/projects/{project_id_or_identifier}/unarchive.json",
        )
        if response.status_code == 204:
            return {"status": "success", "message": "Project unarchived"}
        else:
            return {
                "status": "error",
                "message": response.text,
                "status_code": response.status_code,
            }
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"status": "not_found", "message": "Project not found"}
        raise
