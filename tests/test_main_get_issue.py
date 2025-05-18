import json
import os
import sys
from pprint import pprint

from tools.Issues.get_issue_tool import get_issue


def test_get_issue():
    """Normal case test for Redmine issue retrieval API

    Args:
        None

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
        Change issue_id=1 to an existing issue ID.
    """
    issue_id = 1  # Please specify an existing issue ID
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"

    result = get_issue(
        redmine_url=redmine_url,
        api_key=api_key,
        issue_id=issue_id,
    )
    # Handle cases where a list of TextContent type is returned
    if isinstance(result, list) and hasattr(result[0], "text"):
        result_dict = json.loads(result[0].text)
    else:
        result_dict = result
    pprint(result_dict, stream=sys.stderr)
    assert isinstance(result_dict, dict), "API response is not a dict type"
    assert "issue" in result_dict, "'issue' key does not exist in the response"
    assert result_dict["issue"] is not None, "Issue not found"
    assert result_dict["issue"]["id"] == issue_id, "Retrieved issue ID does not match"


def test_get_issue_notfound():
    """Test for non-existent issue_id (should return {'issue': None})"""
    issue_id = 999999  # unlikely to exist
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"

    result = get_issue(
        redmine_url=redmine_url,
        api_key=api_key,
        issue_id=issue_id,
    )
    if isinstance(result, list) and hasattr(result[0], "text"):
        result_dict = json.loads(result[0].text)
    else:
        result_dict = result
    pprint(result_dict, stream=sys.stderr)
    assert isinstance(result_dict, dict), "API response is not a dict type"
    assert "issue" in result_dict, "'issue' key does not exist in the response"
    assert result_dict["issue"] is None, "Expected 'issue' to be None for non-existent ID"
