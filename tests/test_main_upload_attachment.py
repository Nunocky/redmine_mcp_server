"""Redmine Attachments API アップロードエンドポイントの実機テスト

pytest -s tests/test_main_upload_attachment.py
"""

import os
import sys
import tempfile
from pprint import pprint

import pytest
import requests


def create_temp_file(content: bytes = b"upload test file") -> str:
    """一時ファイルを作成しパスを返す

    Args:
        content (bytes): ファイル内容

    Returns:
        str: 一時ファイルのパス
    """
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    return path


def test_upload_attachment_success():
    """添付ファイルアップロードAPIの正常系テスト

    必要な環境変数:
        REDMINE_URL, REDMINE_USER_API_KEY
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    if not redmine_url or not api_key:
        pytest.fail("REDMINE_URL, REDMINE_USER_API_KEY のいずれかが未設定です")

    file_path = create_temp_file()
    upload_url = f"{redmine_url}/uploads.json"
    with open(file_path, "rb") as f:
        headers = {
            "X-Redmine-API-Key": api_key,
            "Content-Type": "application/octet-stream",
        }
        response = requests.post(upload_url, headers=headers, data=f)
    pprint(response.text, stream=sys.stderr)
    assert response.status_code == 201
    result = response.json()
    assert "upload" in result
    assert "token" in result["upload"]
    assert result["upload"]["token"]

    os.remove(file_path)


def test_upload_attachment_file_not_found():
    """存在しないファイルパス指定時のエラー系テスト

    必要な環境変数:
        REDMINE_URL, REDMINE_USER_API_KEY
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    if not redmine_url or not api_key:
        pytest.fail("REDMINE_URL, REDMINE_USER_API_KEY のいずれかが未設定です")

    file_path = "/tmp/not_exist_file_123456789.txt"
    upload_url = f"{redmine_url}/uploads.json"
    with pytest.raises(FileNotFoundError):
        with open(file_path, "rb") as f:
            headers = {
                "X-Redmine-API-Key": api_key,
                "Content-Type": "application/octet-stream",
            }
            requests.post(upload_url, headers=headers, data=f)
