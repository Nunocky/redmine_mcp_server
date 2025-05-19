"""Attachments API upload_attachment 実機テスト

pytest -s tests/Attachments/test_upload_attachment_tool.py
"""

import os

import pytest

from tools.Attachments.upload_attachment_tool import upload_attachment


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        pytest.fail(f"環境変数 {key} が未設定のため失敗")
    return value


def test_upload_attachment_success():
    """添付ファイルアップロードAPIの正常系テスト"""
    import tempfile

    redmine_url = get_env("REDMINE_URL")
    api_key = get_env("REDMINE_USER_API_KEY") or get_env("REDMINE_ADMIN_API_KEY")

    # 一時ファイル作成
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt") as tmp:
        tmp.write("upload test file\n")
        tmp_path = tmp.name

    try:
        result = upload_attachment(
            redmine_url=redmine_url,
            api_key=api_key,
            file_path=tmp_path,
        )
        print("result:", result)
        assert result["success"] is True
        assert "token" in result
        assert result["token"]
    finally:
        # テスト後にファイル削除
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_upload_attachment_file_not_found():
    """存在しないファイルパス指定時のエラー系テスト"""
    redmine_url = get_env("REDMINE_URL")
    api_key = get_env("REDMINE_USER_API_KEY") or get_env("REDMINE_ADMIN_API_KEY")
    file_path = "/tmp/not_exist_file_123456789.txt"
    result = upload_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        file_path=file_path,
    )
    print("result:", result)
    assert result["success"] is False
    assert "error" in result
