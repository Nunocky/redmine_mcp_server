import os

import pytest
import requests

from tools.Files.create_file import create_file


def upload_file_and_get_token(redmine_url, api_key, filename, content):
    """Redmine /uploads APIでファイルをアップロードし、tokenを取得"""
    url = f"{redmine_url.rstrip('/')}/uploads.json"
    headers = {
        "X-Redmine-API-Key": api_key,
        "Content-Type": "application/octet-stream",
    }
    response = requests.post(
        url,
        headers=headers,
        data=content,
    )
    response.raise_for_status()
    return response.json()["upload"]["token"]


def test_create_file_success():
    """正常系: ファイル登録API"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_ADMIN_API_KEY"]
    project_id = os.environ["REDMINE_TEST_PROJECT_ID"]
    filename = "apitest.txt"
    file_content = "APIテスト用ファイル".encode("utf-8")

    token = upload_file_and_get_token(
        redmine_url=redmine_url,
        api_key=api_key,
        filename=filename,
        content=file_content,
    )
    file = {
        "token": token,
        "filename": filename,
        "description": "APIテスト用ファイル",
    }

    result = create_file(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
        file=file,
    )
    assert isinstance(result, dict)
    # 204 No Content時は空dict、201 Created時はfile情報
    if result:
        assert "file" in result
        assert result["file"]["filename"] == filename


def test_create_file_missing_token():
    """異常系: token未指定"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_ADMIN_API_KEY"]
    project_id = os.environ["REDMINE_TEST_PROJECT_ID"]
    file = {
        # "token": None,
        "filename": "apitest.txt",
        "description": "APIテスト用ファイル",
    }
    with pytest.raises(ValueError):
        create_file(
            redmine_url=redmine_url,
            api_key=api_key,
            project_id=project_id,
            file=file,
        )
