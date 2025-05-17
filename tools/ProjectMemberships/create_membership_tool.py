"""Redmine Project Membership Creation Tool

This tool creates a new project membership in Redmine.
"""

from typing import Any, Dict, List, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def create_membership(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    project_id: str = "",
    user_id: int = 0,
    role_ids: List[int] = [],
):
    """Create a new project membership in Redmine

    Args:
        redmine_url (str): URL of the Redmine server
        api_key (str): Redmine API key
        project_id (str): Project ID or identifier
        user_id (int): User ID to add
        role_ids (List[int]): List of role IDs to assign

    Returns:
        dict: Created membership information or error details

    Raises:
        Exception: When API request fails
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    payload: Dict[str, Any] = {"membership": {"user_id": user_id, "role_ids": role_ids}}

    endpoint = f"/projects/{project_id}/memberships.json"
    try:
        response = client.post(
            endpoint=endpoint,
            json=payload,
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()  # Should be 201 Created for successful membership creation
    except Exception as e:
        # Try to get more detailed error from Redmine if possible
        error_details = {"message": str(e)}
        if hasattr(e, "response") and e.response is not None:
            try:
                error_details["redmine_error"] = e.response.json()
                error_details["status_code"] = e.response.status_code
            except ValueError:  # If response is not JSON
                error_details["redmine_error_text"] = e.response.text
                error_details["status_code"] = e.response.status_code

        # For tests, it's useful to see the original exception type as well
        error_details["exception_type"] = type(e).__name__
        return {"error": error_details}


CreateProjectMembershipTool = Tool.from_function(
    create_membership,
    name="create_project_membership",
    description="Create a new project membership in Redmine",
)
