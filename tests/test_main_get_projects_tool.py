import os
import sys
from pprint import pprint

from main import get_projects_tool
import pytest
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.asyncio
async def test_get_projects_tool():
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_API_KEY is not set in .env"

    result = await get_projects_tool(
        redmine_url=redmine_url,
        api_key=api_key,
        include=None,
        limit=5,
        offset=0
    )
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "projects" in result
    assert isinstance(result["projects"], list)
