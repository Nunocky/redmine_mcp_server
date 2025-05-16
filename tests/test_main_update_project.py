import os
import sys
import random
import string
from pprint import pprint

import pytest
from dotenv import load_dotenv

from main import create_project, update_project, delete_project

load_dotenv()

def random_identifier(prefix="testproj"):
    """一意なidentifierを生成"""
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

@pytest.mark.asyncio
async def test_create_update_delete_project():
    """Redmineプロジェクト作成・更新・削除APIの正常系テスト

    Args:
        なし

    Raises:
        AssertionError: APIレスポンスが期待通りでない場合

    Note:
        REDMINE_URL, REDMINE_ADMIN_API_KEY は .env で設定してください。
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"

    identifier = random_identifier()
    name = "テストプロジェクト_" + identifier
    description = "自動テスト用プロジェクト"

    # プロジェクト作成
    result_create = await create_project(
        name=name,
        identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
        description=description
    )
    pprint(result_create, stream=sys.stderr)
    assert isinstance(result_create, dict)
    assert "id" in result_create
    assert result_create["identifier"] == identifier
    assert result_create["name"] == name
    assert result_create["description"] == description

    # プロジェクト更新
    new_name = name + "_更新"
    new_description = "更新後の説明"
    result_update = await update_project(
        project_id_or_identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key,
        name=new_name,
        description=new_description
    )
    pprint(result_update, stream=sys.stderr)
    # Redmineの仕様上、204 No Contentの場合は空dictとなる
    if result_update:
        assert isinstance(result_update, dict)
        if "name" in result_update:
            assert result_update["name"] == new_name
        if "description" in result_update:
            assert result_update["description"] == new_description

    # プロジェクト削除
    result_delete = await delete_project(
        project_id_or_identifier=identifier,
        redmine_url=redmine_url,
        api_key=api_key
    )
    pprint(result_delete, stream=sys.stderr)
    assert result_delete["status"] == "success"
