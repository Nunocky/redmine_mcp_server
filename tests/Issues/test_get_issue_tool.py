import os

from tools.Issues.get_issue import get_issue

REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")


def test_get_issue_success():
    # Need to set a valid issue_id in advance
    issue_id = 1
    result = get_issue(REDMINE_URL, API_KEY, issue_id)
    assert "issue" in result
    assert result["issue"]["id"] == issue_id


def test_get_issue_notfound():
    # Specify a non-existent ID
    issue_id = 999999
    result = get_issue(REDMINE_URL, API_KEY, issue_id)
    assert "issue" in result
    assert result["issue"] is None
