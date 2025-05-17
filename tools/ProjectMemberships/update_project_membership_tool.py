"""Tool for updating a project membership's roles in Redmine.

This tool uses the RedmineAPIClient to update the roles of a specific membership.

Author: Cline
"""

import os
from typing import List

from tools.redmine_api_client import RedmineAPIClient


class UpdateProjectMembershipTool:
    """Tool to update roles of a project membership in Redmine.

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

    def execute(self, membership_id: int, role_ids: List[int]) -> dict:
        """Update the roles of a project membership.

        Args:
            membership_id (int): The ID of the membership to update.
            role_ids (List[int]): The list of role IDs to assign.

        Returns:
            dict: The updated membership information.

        Raises:
            Exception: If the API call fails or returns an error.
        """
        path = f"/memberships/{membership_id}.json"
        payload = {"membership": {"role_ids": role_ids}}
        try:
            resp = self.client.put(path, json=payload)
            # Redmineの仕様上、204 No Contentの場合は更新成功
            if resp.status_code == 204:
                # 最新情報を取得して返す
                from tools.ProjectMemberships.get_project_membership_tool import GetProjectMembershipTool

                get_tool = GetProjectMembershipTool(client=self.client)
                return get_tool.execute(membership_id)
            data = resp.json()
            if "membership" not in data:
                raise Exception("Invalid response: 'membership' key not found.")
            return data["membership"]
        except Exception as e:
            raise Exception(f"Failed to update project membership: {e}")
