import os
import pytest
from tools.Issues.get_issue_tool import get_issue

from dotenv import load_dotenv
load_dotenv()

REDMINE_URL = os.environ.get("REDMINE_URL")
API_KEY = os.environ.get("REDMINE_ADMIN_API_KEY")

@pytest.mark.skipif(not REDMINE_URL or not API_KEY, reason="Redmine connection information is not set")
def test_get_issue_success():
    # Need to set a valid issue_id in advance
    issue_id = 1
    result = get_issue(REDMINE_URL, API_KEY, issue_id)
    assert "issue" in result
    assert result["issue"]["id"] == issue_id

@pytest.mark.skipif(not REDMINE_URL or not API_KEY, reason="Redmine connection information is not set")
def test_get_issue_notfound():
    # Specify a non-existent ID
    issue_id = 999999
    with pytest.raises(Exception):
        get_issue(REDMINE_URL, API_KEY, issue_id)
