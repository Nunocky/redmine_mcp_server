import os
from pathlib import Path

from tools.Issues.create_issue_tool import CreateIssueTool
from tools.Issues.delete_issue_tool import delete_issue
from tools.Issues.update_issue_tool import update_issue


def setup_module(module):
    pass


async def test_update_issue_redmine():
    """
    Integration test that retrieves information from the actual Redmine server from .env, creates an issue, and updates it.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    project_id = "testproject"
    subject = "Update Test Issue (pytest)"
    description = "Issue for update test by pytest"
    # First, create an issue
    issue = (
        await CreateIssueTool.run(
            {
                "redmine_url": redmine_url,
                "api_key": api_key,
                "project_id": project_id,
                "subject": subject,
                "description": description,
            }
        )
    )["issue"]
    issue_id = issue["id"]
    # Update content
    new_subject = "Updated Issue Title (pytest)"
    new_description = "Issue description has been updated"
    result = update_issue(redmine_url, api_key, issue_id, subject=new_subject, description=new_description)
    print("update_issue result:", result)
    assert result["success"] is True
    # Delete the issue created for the test
    del_result = delete_issue(redmine_url, api_key, issue_id)
    assert del_result["success"] is True
