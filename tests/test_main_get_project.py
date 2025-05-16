import os
import sys
from pprint import pprint

import pytest
from dotenv import load_dotenv

from main import get_project

load_dotenv()

@pytest.mark.asyncio
async def test_get_project():
    """Redmineプロジェクト詳細取得APIの正常系テスト

    Args:
        なし

    Raises:
        AssertionError: APIレスポンスが期待通りでない場合

    Note:
        REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_PROJECT_ID は .env で設定してください。
    """
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    result = await get_project(project_id)
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result

@pytest.mark.asyncio
async def test_get_project_with_include():
    """Redmineプロジェクト詳細取得API（include指定）の正常系テスト

    Args:
        なし

    Raises:
        AssertionError: APIレスポンスが期待通りでない場合

    Note:
        REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_PROJECT_ID は .env で設定してください。
    """
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    assert project_id, "REDMINE_TEST_PROJECT_ID is not set in .env"

    result = await get_project(project_id, include="trackers,enabled_modules")
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "id" in result
    assert "name" in result
    # includeで指定した情報が含まれているか確認
    if "trackers" in result:
        assert isinstance(result["trackers"], list)
    if "enabled_modules" in result:
        assert isinstance(result["enabled_modules"], list)
