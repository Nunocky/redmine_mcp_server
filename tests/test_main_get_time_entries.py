import os
import sys
from pprint import pprint

import pytest

from main import get_time_entries


@pytest.mark.asyncio
async def test_get_time_entries_basic():
    """Basic test for get_time_entries tool via main.py

    Raises:
        AssertionError: If the API response is not as expected

    Note:
        Please set REDMINE_URL and REDMINE_ADMIN_API_KEY in .env.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"

    result = await get_time_entries(
        redmine_url=redmine_url,
        api_key=api_key,
        limit=1,
    )
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "time_entries" in result
