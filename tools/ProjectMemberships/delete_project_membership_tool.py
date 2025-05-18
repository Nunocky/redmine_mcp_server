"""Tool for deleting a project membership in Redmine.

This tool uses the RedmineAPIClient to delete a specific membership.
"""

import os

from tools.redmine_api_client import RedmineAPIClient


class DeleteProjectMembershipTool:
    """Tool to delete a project membership in Redmine.

    Attributes:
        client (RedmineAPIClient): The API client for Redmine.
    """

    def __init__(self, client=None):
        """Initialize the tool with Redmine API client.

        Args:
            client (RedmineAPIClient, optional): Injected API client for testing.
        """
        if client is not None:
            self.client = client
        else:
            redmine_url = os.getenv("REDMINE_URL")
            api_key = os.getenv("REDMINE_ADMIN_API_KEY")
            if not redmine_url or not api_key:
                raise ValueError("REDMINE_URL and REDMINE_ADMIN_API_KEY must be set in environment variables.")
            self.client = RedmineAPIClient(redmine_url, api_key)

    def execute(self, membership_id: int) -> dict:
        """Delete a project membership.

        Args:
            membership_id (int): The ID of the membership to delete.

        Returns:
            dict: Result with status code or error message.

        Raises:
            Exception: If the API call fails or returns an error.
        """
        path = f"/memberships/{membership_id}.json"
        try:
            resp = self.client.delete(path)
            # Redmineの仕様上、204 No Contentの場合は削除成功
            if resp.status_code == 204:
                return {"status": "success", "status_code": 204}
            return {"status": "failed", "status_code": resp.status_code, "message": resp.text}
        except Exception as e:
            # 404エラーなどもstatus: failedで返す
            if hasattr(e, "response") and hasattr(e.response, "status_code"):
                return {"status": "failed", "status_code": e.response.status_code, "message": str(e)}
            return {"status": "failed", "status_code": None, "message": str(e)}
