import os

from tools.Files.get_files import get_files


def test_get_files_success():
    """正常系: プロジェクトのファイル一覧取得"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_USER_API_KEY"]
    project_id = os.environ["REDMINE_TEST_PROJECT_ID"]
    result = get_files(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
    )
    assert isinstance(result, dict)
    assert "files" in result
    assert isinstance(result["files"], list)


def test_get_files_not_found():
    """異常系: 存在しないプロジェクトID"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_USER_API_KEY"]
    project_id = "not_exist_project_12345"
    result = get_files(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
    )
    assert isinstance(result, dict)
    assert "files" in result
    assert result["files"] == []
