import os
import sys
from pprint import pprint

import pytest

from main import get_queries_tool


@pytest.mark.asyncio
async def test_get_queries():
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"

    result = await get_queries_tool(redmine_url=redmine_url, api_key=api_key)
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "queries" in result
    assert isinstance(result["queries"], list)
