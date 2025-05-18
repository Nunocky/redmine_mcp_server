"""Redmine Project Membership Creation Tool

This tool creates a new project membership in Redmine.
Returns error details for HTTP errors.

Returns:
    dict: Created membership information or error details

Raises:
    Exception: When API request fails (excluding HTTP errors)
"""

from typing import Any, Dict, List

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def create_membership(
    redmine_url: str,
    api_key: str,
    project_id: str,
    user_id: int,
    role_ids: List[int],
) -> Dict[str, Any]:
    """Create a new project membership in Redmine

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        project_id: Project ID or identifier
        user_id: User ID to add
        role_ids: List of role IDs to assign

    Returns:
        Created membership information or error details (for HTTP errors)

    Raises:
        Exception: When API request fails (excluding HTTP errors)
    """
    # Create Redmine API client
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    payload: Dict[str, Any] = {"membership": {"user_id": user_id, "role_ids": role_ids}}
    endpoint = f"/projects/{project_id}/memberships.json"
    try:
        response = client.post(
            endpoint=endpoint,
            json=payload,
        )
        data = response.json()
        return {
            "membership": data.get("membership", {}),
        }
    except requests.exceptions.HTTPError as e:
        # Return error details for HTTP errors
        error_details = {"message": str(e)}
        if e.response is not None:
            try:
                error_details["redmine_error"] = e.response.json()
                error_details["status_code"] = e.response.status_code
            except Exception:
                error_details["redmine_error_text"] = e.response.text
                error_details["status_code"] = e.response.status_code
        error_details["exception_type"] = type(e).__name__
        return {"error": error_details}
    except Exception as e:
        # Raise other exceptions
        raise


CreateProjectMembershipTool = Tool.from_function(
    create_membership,
    name="create_project_membership",
    description="Create a new project membership in Redmine",
)
