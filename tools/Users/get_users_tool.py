"""Redmine User List Retrieval Tool

This tool retrieves a list of users from Redmine.
"""

from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


class GetUsersTool:
    """Redmine User List Retrieval Tool

    Attributes:
        client (RedmineAPIClient): Redmine API client
    """

    def __init__(self, client: Optional[RedmineAPIClient] = None) -> None:
        """Constructor

        Args:
            client (RedmineAPIClient, optional): API client. If not specified, a new one is generated.
        """
        self.client = client or RedmineAPIClient()

    def run(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[int] = None,
        name: Optional[str] = None,
        group_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get a list of users

        Args:
            limit (int, optional): Number of items to retrieve
            offset (int, optional): Number of items to skip
            status (int, optional): User status (1: active, 2: registered, 3: locked)
            name (str, optional): Filter by login name, first name, last name, or email address
            group_id (int, optional): Filter by users belonging to a specific group

        Returns:
            dict: User list and page information

        Raises:
            Exception: When API request fails
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status
        if name is not None:
            params["name"] = name
        if group_id is not None:
            params["group_id"] = group_id

        response = self.client.get(
            endpoint="/users.json",
            params=params,
        )
        data = response.json()
        return {
            "users": data.get("users", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
