import os

from tools.Issues.create_issue_tool import create_issue

REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")


def test_create_issue_redmine():
    """
    Integration test to create a new issue on the actual Redmine server (REDMINE_URL in .env).
    """
    project_id = "testproject"
    subject = "Test Issue (pytest)"
    description = "Automated test creation by pytest"
    result = create_issue(
        redmine_url=REDMINE_URL,
        api_key=API_KEY,
        project_id=project_id,
        subject=subject,
        description=description,
    )
    assert "issue" in result
    assert isinstance(result["issue"], dict)
    assert result["issue"].get("subject") == subject
