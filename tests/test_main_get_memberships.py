import os
import sys
from pprint import pprint

from main import get_memberships
import pytest
from dotenv import load_dotenv


load_dotenv()


@pytest.mark.asyncio
async def test_get_memberships_tool():
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_API_KEY is not set in .env"

    # 実際のAPI呼び出し（引数は適宜調整）
    result = await get_memberships(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id="1",
    )
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "memberships" in result
    assert isinstance(result["memberships"], list)
