"""Redmine Issue Creation Tool

This tool creates a new Redmine issue.
"""

from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


class CreateIssueTool:
    """Redmine Issue Creation Tool

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
        project_id: str,
        subject: str,
        description: Optional[str] = None,
        tracker_id: Optional[int] = None,
        status_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        category_id: Optional[int] = None,
        fixed_version_id: Optional[int] = None,
        assigned_to_id: Optional[int] = None,
        parent_issue_id: Optional[int] = None,
        custom_fields: Optional[Any] = None,
        watcher_user_ids: Optional[Any] = None,
        is_private: Optional[bool] = None,
        estimated_hours: Optional[float] = None,
        uploads: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Create a new issue

        Args:
            project_id (str): Project ID
            subject (str): Subject
            description (str, optional): Description
            tracker_id (int, optional): Tracker ID
            status_id (int, optional): Status ID
            priority_id (int, optional): Priority ID
            category_id (int, optional): Category ID
            fixed_version_id (int, optional): Version ID
            assigned_to_id (int, optional): Assignee ID
            parent_issue_id (int, optional): Parent issue ID
            custom_fields (Any, optional): Custom fields
            watcher_user_ids (Any, optional): List of watcher IDs
            is_private (bool, optional): Private flag
            estimated_hours (float, optional): Estimated hours
            uploads (Any, optional): Attached files

        Returns:
            dict: Information of the created issue

        Raises:
            Exception: When API request fails
        """
        issue_data: Dict[str, Any] = {
            "project_id": project_id,
            "subject": subject,
        }
        if description:
            issue_data["description"] = description
        if tracker_id is not None:
            issue_data["tracker_id"] = tracker_id
        if status_id is not None:
            issue_data["status_id"] = status_id
        if priority_id is not None:
            issue_data["priority_id"] = priority_id
        if category_id is not None:
            issue_data["category_id"] = category_id
        if fixed_version_id is not None:
            issue_data["fixed_version_id"] = fixed_version_id
        if assigned_to_id is not None:
            issue_data["assigned_to_id"] = assigned_to_id
        if parent_issue_id is not None:
            issue_data["parent_issue_id"] = parent_issue_id
        if custom_fields:
            issue_data["custom_fields"] = custom_fields
        if watcher_user_ids:
            issue_data["watcher_user_ids"] = watcher_user_ids
        if is_private is not None:
            issue_data["is_private"] = is_private
        if estimated_hours is not None:
            issue_data["estimated_hours"] = estimated_hours
        if uploads:
            issue_data["uploads"] = uploads

        response = self.client.post(
            endpoint="/issues.json",
            json={"issue": issue_data},
        )
        return response.json()
