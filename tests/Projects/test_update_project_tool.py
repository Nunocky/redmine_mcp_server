import os
import pytest
import pprint
import dotenv
import random
import string
from tools.Projects.create_project_tool import create_project
from tools.Projects.update_project_tool import update_project
from tools.Projects.delete_project_tool import delete_project

dotenv.load_dotenv()

def random_identifier(prefix="testproj"):
    """一意なidentifierを生成"""
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def test_create_update_delete_project_real_api():
    """実API: プロジェクト作成→更新→削除"""
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

    # プロジェクト更新
    new_name = name + "_更新"
    new_description = "更新後の説明"
    result_update = update_project(
        identifier,
        redmine_url=redmine_url,
        api_key=api_key,
        name=new_name,
        description=new_description
    )
    pprint.pprint(result_update)
    # Redmineの仕様上、204 No Contentの場合は空dictとなる
    if result_update:
        assert "id" in result_update
        assert result_update["name"] == new_name
        assert result_update["description"] == new_description
    else:
        # 空dictなら更新成功とみなす
        assert result_update == {}

    # プロジェクト削除
    result_delete = delete_project(
        identifier,
        redmine_url=redmine_url,
        api_key=api_key
    )
    pprint.pprint(result_delete)
    assert result_delete["status"] == "success"
