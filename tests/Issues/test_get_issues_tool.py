"""Tests for GetIssuesTool

Verify the behavior of the Redmine issue list retrieval API using GetIssuesTool.
"""

import os

from dotenv import load_dotenv

from tools.Issues.get_issues_tool import get_issues

load_dotenv()


def test_get_issues_basic():
    """Verify that the issue list can be retrieved

    Returns:
        None
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = get_issues(
        redmine_url=redmine_url,
        api_key=api_key,
        limit=5,
    )
    assert "issues" in result
    assert isinstance(result["issues"], list)
    assert len(result["issues"]) <= 5
    assert "total_count" in result
    assert "offset" in result
    assert "limit" in result


def test_get_issues_with_filters():
    """Verify that the issue list can be retrieved with filters

    Returns:
        None
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    filters = {"status_id": "open"}
    result = get_issues(
        redmine_url=redmine_url,
        api_key=api_key,
        limit=3,
        filters=filters,
    )
    assert "issues" in result
    for issue in result["issues"]:
        # Consider cases where status names are in Japanese
        assert issue["status"]["name"] in ["New", "Open", "新規", "進行中"]


def test_get_issues_with_offset_and_limit():
    """Verify that paging can be done with offset and limit"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = get_issues(
        redmine_url=redmine_url,
        api_key=api_key,
        offset=2,
        limit=2,
    )
    assert "issues" in result
    assert len(result["issues"]) <= 2
    assert result["offset"] == 2


def test_get_issues_with_sort():
    """Verify that sorting can be done with the sort parameter"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = get_issues(
        redmine_url=redmine_url,
        api_key=api_key,
        sort="updated_on:desc",
        limit=3,
    )
    dates = [issue["updated_on"] for issue in result["issues"]]
    assert dates == sorted(dates, reverse=True)


def test_get_issues_with_include():
    """Verify that attachments etc. can be retrieved with the include parameter"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = get_issues(
        redmine_url=redmine_url,
        api_key=api_key,
        include="attachments",
        limit=1,
    )
    assert "issues" in result
    for issue in result["issues"]:
        assert "attachments" in issue


def test_get_issues_with_multiple_filters():
    """Verify that filtering can be done with multiple filters"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    filters = {"project_id": 1, "tracker_id": 2}
    result = get_issues(
        redmine_url=redmine_url,
        api_key=api_key,
        filters=filters,
        limit=2,
    )
    for issue in result["issues"]:
        assert issue["project"]["id"] == 1
        assert issue["tracker"]["id"] == 2


def test_get_issues_with_invalid_filter():
    """Verify that 0 items are returned for non-existent project_id etc."""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    filters = {"project_id": 999999}
    result = get_issues(
        redmine_url=redmine_url,
        api_key=api_key,
        filters=filters,
    )
    assert result["total_count"] == 0


def test_get_issues_api_error(monkeypatch):
    """Verify that an exception is raised in case of API error"""

    def mock_get(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.status_code = 404

            def raise_for_status(self):
                from requests.exceptions import HTTPError

                raise HTTPError(f"404 Client Error: Not Found for url: {kwargs.get('url', '')}")

        return MockResponse()

    monkeypatch.setattr("tools.redmine_api_client.RedmineAPIClient.get", mock_get)
    try:
        get_issues(
            redmine_url="dummy",
            api_key="dummy",
        )
        assert False, "Exception not raised"
    except Exception:
        assert True
