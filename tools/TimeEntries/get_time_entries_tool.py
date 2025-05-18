"""Tool class for retrieving Redmine TimeEntries list via REST API.

This tool fetches a list of time entries from Redmine using the REST API.
"""

from typing import Any, Dict, Optional

import requests


class GetTimeEntriesTool:
    """
    Tool for retrieving a list of Redmine TimeEntries.

    Example:
        tool = GetTimeEntriesTool()
        result = tool.run(
            redmine_url="http://localhost:3000",
            api_key="xxxxxxxx",
            limit=10,
            project_id="myproject"
        )
    """

    def run(
        self,
        redmine_url: str,
        api_key: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        user_id: Optional[int] = None,
        project_id: Optional[str] = None,
        spent_on: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Execute the tool to retrieve time entries.

        Args:
            redmine_url (str): Redmine base URL.
            api_key (str): Redmine REST API key.
            offset (Optional[int]): Offset for pagination.
            limit (Optional[int]): Limit for pagination.
            user_id (Optional[int]): Filter by user ID.
            project_id (Optional[str]): Filter by project ID or identifier.
            spent_on (Optional[str]): Filter by spent date.
            from_date (Optional[str]): Filter by start date.
            to_date (Optional[str]): Filter by end date.

        Returns:
            dict: API response containing time entries list.

        Raises:
            Exception: If the API request fails or returns an error.
        """
        headers = {"X-Redmine-API-Key": api_key}
        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if user_id is not None:
            params["user_id"] = user_id
        if project_id is not None:
            params["project_id"] = project_id
        if spent_on is not None:
            params["spent_on"] = spent_on
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date

        url = f"{redmine_url.rstrip('/')}/time_entries.json"
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            raise Exception(f"Failed to get time entries: {response.status_code} {response.text}")
        return response.json()
