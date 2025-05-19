"""Redmine Project Deletion Tool

Delete a project using RedmineAPIClient.
Returns {"status": "success", "message": "..."} for 204 No Content,
{"status": "error", "message": "..."} for 404 error,
{"status": "error", "message": "..."} for other errors.

Returns:
    dict: {"status": "success", "message": "..."} if deleted (204), {"status": "error", "message": "..."} for errors

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def delete_project(
    project_id_or_identifier: str,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Delete a Redmine project

    Args:
        project_id_or_identifier: Project ID or identifier
        redmine_url: URL of the Redmine server
        api_key: Redmine API key

    Returns:
        {"status": "success", "message": "..."} if deleted (204), {"status": "error", "message": "..."} for errors

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/projects/{project_id_or_identifier}.json"
    try:
        response = client.delete(endpoint)
        if response.status_code == 204:
            return {"status": "success", "message": "Project deleted"}
        return {
            "status": "error",
            "message": response.text or f"Unexpected status code: {response.status_code}",
            "status_code": response.status_code,
        }
    except requests.exceptions.HTTPError as e:
        return {
            "status": "error",
            "message": str(e),
            "status_code": getattr(e.response, "status_code", 500),
        }


DeleteProjectTool = Tool.from_function(
    delete_project,
    name="delete_project",
    description="Delete a Redmine project",
)
