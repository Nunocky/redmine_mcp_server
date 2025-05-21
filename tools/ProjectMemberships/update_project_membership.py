"""Tool for updating a project membership's roles in Redmine.

This tool uses the RedmineAPIClient to update the roles of a specific membership.
"""

import os
from typing import List

from tools.redmine_api_client import RedmineAPIClient


class UpdateProjectMembershipTool:
    """Tool to update roles of a project membership in Redmine.

    Attributes:
        client (RedmineAPIClient): Redmine API client instance.

    Example:
        tool = UpdateProjectMembershipTool()
        result = tool.execute(membership_id=1, role_ids=[2, 3])
    """

    def __init__(self, client=None):
        """Initialize UpdateProjectMembershipTool.

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

    def execute(self, membership_id: int, role_ids: List[int]) -> dict:
        """Update the roles of a project membership.

        Args:
            membership_id (int): Membership ID to update.
            role_ids (List[int]): List of role IDs to assign.

        Returns:
            dict: Updated membership information.

        Raises:
            Exception: If the API call fails or returns an error.
        """
        path = f"/memberships/{membership_id}.json"
        payload = {"membership": {"role_ids": role_ids}}
        try:
            resp = self.client.put(path, json=payload)
            # According to Redmine API, 204 No Content means update succeeded.
            if resp.status_code == 204:
                # Retrieve latest membership info after update.
                from tools.ProjectMemberships.get_project_membership import GetProjectMembershipTool

                get_tool = GetProjectMembershipTool(client=self.client)
                return get_tool.execute(membership_id)
            data = resp.json()
            if "membership" not in data:
                raise Exception(f"Invalid API response: 'membership' key not found. Response content: {data}")
            return data["membership"]
        except Exception as e:
            raise Exception(f"Failed to update project membership (ID: {membership_id}, roles: {role_ids}): {e}") from e
