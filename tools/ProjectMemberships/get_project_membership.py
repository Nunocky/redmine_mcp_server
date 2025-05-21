"""Tool for retrieving the details of a specific project membership from Redmine.

This tool uses the RedmineApiClient to access the Redmine REST API and fetch
membership details by membership ID.
"""

import os

from tools.redmine_api_client import RedmineAPIClient


class GetProjectMembershipTool:
    """Tool to get details of a project membership from Redmine.

    Attributes:
        client (RedmineApiClient): The API client for Redmine.
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
        """Get the details of a project membership.

        Args:
            membership_id (int): The ID of the membership to retrieve.

        Returns:
            dict: The membership detail information.

        Raises:
            Exception: If the API call fails or returns an error.
        """
        # Build the API endpoint path
        path = f"/memberships/{membership_id}.json"
        try:
            resp = self.client.get(path)
            # The Redmine API returns a requests.Response object
            data = resp.json()
            if "membership" not in data:
                raise Exception("Invalid response: 'membership' key not found.")
            return data["membership"]
        except Exception as e:
            # Log or handle error as needed
            raise Exception(f"Failed to get project membership detail: {e}")
