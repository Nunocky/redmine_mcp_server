import os
from pathlib import Path

from dotenv import load_dotenv

from tools.Issues.create_issue_tool import CreateIssueTool
from tools.Issues.delete_issue_tool import delete_issue


def setup_module(module):
    # Load .env file by specifying its absolute path
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


def test_delete_issue_real_redmine():
    """
    Integration test that retrieves information from the actual Redmine server from .env, creates an issue, and deletes it.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    project_id = "testproject"
    subject = "Deletion Test Issue (pytest)"
    description = "Issue for deletion test by pytest"
    # First, create an issue
    issue_tool = CreateIssueTool()
    issue = issue_tool.run(project_id, subject, description=description)["issue"]
    issue_id = issue["id"]
    # Execute deletion
    result = delete_issue(redmine_url, api_key, issue_id)
    assert result["success"] is True
