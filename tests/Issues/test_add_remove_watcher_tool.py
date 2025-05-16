import os
from pathlib import Path

from dotenv import load_dotenv

from tools.Issues.create_issue_tool import CreateIssueTool
from tools.Issues.delete_issue_tool import delete_issue
from tools.Issues.add_watcher_tool import add_watcher
from tools.Issues.remove_watcher_tool import remove_watcher

def setup_module(module):
    # Load .env file by specifying its absolute path
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def test_add_remove_watcher_real_redmine():
    """
    Integration test to add and remove a watcher from an issue on a real Redmine server.
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    watcher_user_id = os.getenv("REDMINE_WATCHER_USER_ID")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert watcher_user_id, "REDMINE_WATCHER_USER_ID is not set in .env"
    project_id = "testproject"
    subject = "Watcher Test Issue (pytest)"
    description = "Issue for testing watcher addition and removal by pytest"
    # Create issue
    issue_tool = CreateIssueTool()
    issue = issue_tool.run(project_id, subject, description=description)["issue"]
    issue_id = issue["id"]
    # Add watcher
    add_result = add_watcher(redmine_url, api_key, issue_id, int(watcher_user_id))
    print("add_watcher result:", add_result)
    assert add_result["success"] is True
    # Remove watcher
    remove_result = remove_watcher(redmine_url, api_key, issue_id, int(watcher_user_id))
    print("remove_watcher result:", remove_result)
    assert remove_result["success"] is True
    # Cleanup: Delete issue
    del_result = delete_issue(redmine_url, api_key, issue_id)
    assert del_result["success"] is True
