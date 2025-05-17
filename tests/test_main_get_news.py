import os
import sys
from pprint import pprint

import pytest
from dotenv import load_dotenv

from main import get_news

load_dotenv()


@pytest.mark.asyncio
async def test_get_news():
    """Test get_news for all projects with real Redmine server.

    This test requires the following environment variables:
        - REDMINE_URL
        - REDMINE_ADMIN_API_KEY
        - REDMINE_TEST_PROJECT_ID

    The test will fetch news for all projects and check the response structure.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    # Fetch news for all projects (project_id is not used for all-projects)
    result = await get_news(
        redmine_url=redmine_url,
        api_key=api_key,
        limit=5,
        offset=0,
    )
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "news" in result
    assert isinstance(result["news"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result
