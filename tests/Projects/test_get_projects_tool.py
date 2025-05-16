import os
import pprint

import pytest
from dotenv import load_dotenv

from tools.Projects.get_projects_tool import get_projects

load_dotenv()


def test_get_projects_real_api():
    """実API: パラメータなしでプロジェクト一覧取得"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("REDMINE_URLまたはREDMINE_ADMIN_API_KEYが未設定のためスキップ")
    result = get_projects(redmine_url, api_key)
    pprint.pprint(result)
    assert "projects" in result
    assert "total_count" in result
    assert isinstance(result["projects"], list)
    assert isinstance(result["total_count"], int)

def test_get_projects_with_params_real_api():
    """実API: limit, offset, includeパラメータ指定"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("REDMINE_URLまたはREDMINE_ADMIN_API_KEYが未設定のためスキップ")
    result = get_projects(redmine_url, api_key, limit=2, offset=1, include="trackers,enabled_modules")
    pprint.pprint(result)
    assert "projects" in result
    assert "limit" in result
    assert "offset" in result
    assert result["limit"] == 2
    assert result["offset"] == 1
