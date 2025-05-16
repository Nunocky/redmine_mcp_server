"""Redmine Project Unarchival Tool

Unarchive a project using RedmineAPIClient.
"""

from typing import Any, Dict, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def unarchive_project(
    project_id_or_identifier: str, redmine_url: Optional[str] = None, api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Unarchive a Redmine project

    Args:
        project_id_or_identifier (str): Project ID or identifier
        redmine_url (str, optional): URL of the Redmine server
        api_key (str, optional): Redmine API key

    Returns:
        dict: Unarchival result (status, message)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/projects/{project_id_or_identifier}/unarchive.json"
    resp = client.put(endpoint)
    if resp.status_code == 204:
        return {"status": "success", "message": "Project unarchived"}
    else:
        return {"status": "error", "message": resp.text, "status_code": resp.status_code}


UnarchiveProjectTool = Tool.from_function(
    unarchive_project, name="unarchive_project", description="Unarchive a Redmine project"
)
