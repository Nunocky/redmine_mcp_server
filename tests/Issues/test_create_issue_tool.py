import os
from pathlib import Path

from dotenv import load_dotenv

from tools.Issues.create_issue_tool import CreateIssueTool

# Load .env file by specifying its absolute path
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


def test_create_issue_real_redmine():
    """
    Integration test to create a new issue on the actual Redmine server (REDMINE_URL in .env).
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    project_id = "testproject"
    subject = "Test Issue (pytest)"
    description = "Automated test creation by pytest"
    result = CreateIssueTool().run(project_id, subject, description=description)
    assert "issue" in result
    assert isinstance(result["issue"], dict)
    assert result["issue"].get("subject") == subject
