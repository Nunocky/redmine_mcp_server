import os

from tools.Issues.create_issue import create_issue
from tools.Issues.delete_issue import delete_issue

REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")


def test_delete_issue_redmine():
    """
    Integration test that retrieves information from the actual Redmine server from .env, creates an issue, and deletes it.
    """
    project_id = "testproject"
    subject = "Deletion Test Issue (pytest)"
    description = "Issue for deletion test by pytest"

    # First, create an issue
    result = create_issue(
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
        project_id=project_id,
        subject=subject,
        description=description,
    )
    issue = result["issue"]
    issue_id = issue["id"]

    # Execute deletion
    result = delete_issue(
        REDMINE_URL,
        API_KEY,
        issue_id,
    )
    assert result["success"] is True
