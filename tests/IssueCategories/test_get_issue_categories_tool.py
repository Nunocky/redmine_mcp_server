import os

import pytest

from tools.IssueCategories.get_issue_categories import get_issue_categories


def test_get_issue_categories_normal():
    """Test normal case for get_issue_categories."""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_ADMIN_API_KEY"]
    project_id = os.environ["REDMINE_TEST_PROJECT_ID"]

    result = get_issue_categories(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
    )
    assert "issue_categories" in result
    assert isinstance(result["issue_categories"], list)


def test_get_issue_categories_not_found():
    """Test 404 case for get_issue_categories."""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_ADMIN_API_KEY"]
    project_id = "nonexistent_project_id_404"

    result = get_issue_categories(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
    )
    assert "issue_categories" in result
    assert result["issue_categories"] == []
