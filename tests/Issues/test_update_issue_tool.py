import os

from tools.Issues.create_issue import create_issue
from tools.Issues.delete_issue import delete_issue
from tools.Issues.update_issue import update_issue

REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")


def test_update_issue_redmine():
    """
    Integration test that retrieves information from the actual Redmine server from .env, creates an issue, and updates it.
    """
    project_id = "testproject"
    subject = "Update Test Issue (pytest)"
    description = "Issue for update test by pytest"

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

    # Update content
    new_subject = "Updated Issue Title (pytest)"
    new_description = "Issue description has been updated"
    result = update_issue(
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
        issue_id=issue_id,
        subject=new_subject,
        description=new_description,
    )
    print("update_issue result:", result)
    assert result["success"] is True

    # Delete the issue created for the test
    del_result = delete_issue(
        REDMINE_URL,
        API_KEY,
        issue_id,
    )
    assert del_result["success"] is True
