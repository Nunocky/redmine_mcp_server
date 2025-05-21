"""Redmine Project Archival Tool

Archive a project using RedmineAPIClient.
"""

from typing import Any, Dict, Optional

import requests

from tools.redmine_api_client import RedmineAPIClient


def archive_project(
    redmine_url: str,
    api_key: str,
    project_id_or_identifier: str,
) -> Dict[str, Any]:
    """Archive a Redmine project

    Args:
        project_id_or_identifier (str): Project ID or identifier
        redmine_url (str, optional): URL of the Redmine server
        api_key (str, optional): Redmine API key

    Returns:
        dict: Archival result (status, message)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/projects/{project_id_or_identifier}/archive.json"

    try:
        resp = client.put(endpoint)
        if resp.status_code == 204:
            return {"status": "success"}
        else:
            return {
                "status": "error",
                "message": resp.text,
                "status_code": resp.status_code,
            }
    except requests.exceptions.HTTPError as e:
        return {
            "status": "error",
            "message": str(e),
            "status_code": getattr(e.response, "status_code", None),
        }
