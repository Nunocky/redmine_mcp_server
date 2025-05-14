import os
import pytest
import pprint
import dotenv
from tools.get_project_tool import get_project

dotenv.load_dotenv()

def test_get_project_by_id_real_api():
    """実API: プロジェクトIDで詳細取得"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_API_KEY")
    project_id = os.environ.get("REDMINE_PROJECT_ID")
    print(f"REDMINE_URL={redmine_url}, REDMINE_API_KEY={'***' if api_key else ''}, REDMINE_PROJECT_ID={project_id}")
    if not redmine_url or not api_key or not project_id:
        pytest.skip("REDMINE_URL, REDMINE_API_KEY, REDMINE_PROJECT_IDが未設定のためスキップ")
    result = get_project(project_id, redmine_url, api_key)
    pprint.pprint(result)
    assert "id" in result
    assert "name" in result

def test_get_project_by_identifier_real_api():
    """実API: プロジェクトidentifierで詳細取得"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_API_KEY")
    project_identifier = os.environ.get("REDMINE_PROJECT_IDENTIFIER")
    print(f"REDMINE_URL={redmine_url}, REDMINE_API_KEY={'***' if api_key else ''}, REDMINE_PROJECT_IDENTIFIER={project_identifier}")
    if not redmine_url or not api_key or not project_identifier:
        pytest.skip("REDMINE_URL, REDMINE_API_KEY, REDMINE_PROJECT_IDENTIFIERが未設定のためスキップ")
    result = get_project(project_identifier, redmine_url, api_key)
    pprint.pprint(result)
    assert "id" in result
    assert "name" in result

def test_get_project_with_include_real_api():
    """実API: includeパラメータ指定で詳細取得"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_API_KEY")
    project_id = os.environ.get("REDMINE_PROJECT_ID")
    print(f"REDMINE_URL={redmine_url}, REDMINE_API_KEY={'***' if api_key else ''}, REDMINE_PROJECT_ID={project_id}")
    if not redmine_url or not api_key or not project_id:
        pytest.skip("REDMINE_URL, REDMINE_API_KEY, REDMINE_PROJECT_IDが未設定のためスキップ")
    result = get_project(project_id, redmine_url, api_key, include="trackers,enabled_modules")
    pprint.pprint(result)
    assert "id" in result
    assert "name" in result
