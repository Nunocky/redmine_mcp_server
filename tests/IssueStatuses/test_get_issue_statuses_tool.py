"""Tests for GetIssueStatusesTool

Verify the behavior of the Redmine issue status list retrieval API using GetIssueStatusesTool.
"""

import os

from tools.IssueStatuses.get_issue_statuses import get_issue_statuses


def test_get_issue_statuses_basic():
    """Verify that the issue status list can be retrieved

    Returns:
        None
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = get_issue_statuses(
        redmine_url=redmine_url,
        api_key=api_key,
    )
    assert isinstance(result, list)
    assert len(result) > 0
    for status in result:
        assert "id" in status
        assert "name" in status
        assert "is_closed" in status
        assert isinstance(status["id"], int)
        assert isinstance(status["name"], str)
        assert isinstance(status["is_closed"], bool)
