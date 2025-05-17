import os
import pprint

import pytest
from dotenv import load_dotenv

from tools.Projects.get_projects_tool import get_projects

load_dotenv()


def test_get_projects_real_api():
    """Real API: Get project list without parameters"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("Skipping because REDMINE_URL or REDMINE_ADMIN_API_KEY is not set")
    result = get_projects(redmine_url, api_key)
    pprint.pprint(result)
    assert "projects" in result
    assert "total_count" in result
    assert isinstance(result["projects"], list)
    assert isinstance(result["total_count"], int)


def test_get_projects_with_params_real_api():
    """Real API: Specify limit, offset, and include parameters"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("Skipping because REDMINE_URL or REDMINE_ADMIN_API_KEY is not set")
    result = get_projects(redmine_url, api_key, limit=2, offset=1, include="trackers,enabled_modules")
    pprint.pprint(result)
    assert "projects" in result
    assert "limit" in result
    assert "offset" in result
    assert result["limit"] == 2
    assert result["offset"] == 1
