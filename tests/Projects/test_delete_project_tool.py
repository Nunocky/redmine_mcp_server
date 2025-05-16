import os
import pytest
import pprint
import dotenv
import random
import string
from tools.Projects.create_project_tool import create_project
from tools.Projects.delete_project_tool import delete_project

dotenv.load_dotenv()

def random_identifier(prefix="testproj"):
    """一意なidentifierを生成"""
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def test_delete_project_real_api():
    """実API: プロジェクト削除のテスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("REDMINE_URL, REDMINE_ADMIN_API_KEYが未設定のためスキップ")

    identifier = random_identifier()
    name = "テスト削除用プロジェクト_" + identifier

    # プロジェクト作成
    result_create = create_project(
        name=name,
        identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
        description="削除テスト用プロジェクト"
    )
    pprint.pprint(result_create)
    assert "id" in result_create
    assert result_create["identifier"] == identifier

    # プロジェクト削除
    result_delete = delete_project(
        identifier,
        redmine_url=redmine_url,
        api_key=api_key
    )
    pprint.pprint(result_delete)
    assert result_delete["status"] == "success"
    assert result_delete["message"] == "Project deleted"

def test_delete_nonexistent_project_real_api():
    """実API: 存在しないプロジェクトの削除テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("REDMINE_URL, REDMINE_ADMIN_API_KEYが未設定のためスキップ")

    # 存在しないプロジェクトIDを指定
    nonexistent_id = "nonexistent_project_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # プロジェクト削除
    result_delete = delete_project(
        nonexistent_id,
        redmine_url=redmine_url,
        api_key=api_key
    )
    pprint.pprint(result_delete)
    assert result_delete["status"] == "error"
    assert "status_code" in result_delete
