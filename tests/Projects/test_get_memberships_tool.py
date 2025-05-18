import os
import sys
from pprint import pprint

from tools.ProjectMemberships.get_memberships_tool import get_memberships


def test_get_memberships():
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    result = get_memberships(redmine_url=redmine_url, api_key=api_key, project_id=project_id)
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "memberships" in result
    assert isinstance(result["memberships"], list)
