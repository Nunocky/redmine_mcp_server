import os
import pytest
import pprint
import dotenv
import random
import string
from tools.Projects.create_project_tool import create_project
from tools.Projects.archive_project_tool import archive_project
from tools.Projects.unarchive_project_tool import unarchive_project
from tools.Projects.delete_project_tool import delete_project

dotenv.load_dotenv()

def random_identifier(prefix="testproj"):
    """一意なidentifierを生成"""
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def test_create_archive_unarchive_delete_project_real_api():
    """実API: プロジェクト作成→アーカイブ→アーカイブ解除→削除"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        pytest.skip("REDMINE_URL, REDMINE_ADMIN_API_KEYが未設定のためスキップ")

    identifier = random_identifier()
    name = "テストプロジェクト_" + identifier

    # プロジェクト作成
    result_create = create_project(
        name=name,
        identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
        description="自動テスト用プロジェクト"
    )
    pprint.pprint(result_create)
    assert "id" in result_create
    assert result_create["identifier"] == identifier

    # プロジェクトアーカイブ
    result_archive = archive_project(
        identifier,
        redmine_url=redmine_url,
        api_key=api_key
    )
    pprint.pprint(result_archive)
    assert result_archive["status"] == "success"

    # プロジェクトアーカイブ解除
    result_unarchive = unarchive_project(
        identifier,
        redmine_url=redmine_url,
        api_key=api_key
    )
    pprint.pprint(result_unarchive)
    assert result_unarchive["status"] == "success"

    # プロジェクト削除
    result_delete = delete_project(
        identifier,
        redmine_url=redmine_url,
        api_key=api_key
    )
    pprint.pprint(result_delete)
    assert result_delete["status"] == "success"
