"""Attachments API delete_attachment 実機テスト

pytest -s tests/Attachments/test_delete_attachment_tool.py
"""

import os
import tempfile

import pytest

from tools.Attachments.delete_attachment_tool import delete_attachment
from tools.Attachments.upload_attachment_tool import upload_attachment
from tools.Issues.create_issue_tool import create_issue


def get_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        pytest.fail(f"環境変数 {key} が未設定のため終了")
    return value


def create_temp_file(content: bytes = b"delete test file") -> str:
    """一時ファイルを作成しパスを返す"""
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    return path


def test_delete_attachment_success():
    """添付ファイル削除APIの正常系テスト（事前にアップロード & チケット登録）"""
    redmine_url = get_env("REDMINE_URL")
    api_key = get_env("REDMINE_ADMIN_API_KEY")
    project_id = get_env("REDMINE_TEST_PROJECT_ID")
    # 一時ファイルを作成してアップロード
    file_path = create_temp_file()
    upload_result = upload_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        file_path=file_path,
    )
    print("upload_result:", upload_result)
    assert upload_result["success"] is True
    token = upload_result["token"]
    # チケット作成時にuploadsで添付登録
    uploads = [
        {
            "token": token,
            "filename": os.path.basename(file_path),
            "content_type": "application/octet-stream",
        }
    ]
    issue_result = create_issue(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
        subject="delete attachment test",
        uploads=uploads,
    )
    print("issue_result:", issue_result)
    attachments = issue_result.get("issue", {}).get("attachments", [])
    assert attachments, "チケット作成時に添付ファイルが登録されていません"
    attachment_id = attachments[0]["id"]
    # 削除API実行
    result = delete_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        attachment_id=attachment_id,
    )
    print("delete_result:", result)
    assert result["success"] is True
    assert result["status_code"] in (200, 204)
    # ファイル削除
    os.remove(file_path)


def test_delete_attachment_permission_denied():
    """一般ユーザーは添付ファイルを削除できないことを確認

    - 管理者権限で添付ファイル付きチケットを作成
    - 添付ファイルIDを取得
    - 一般ユーザーAPIキーで削除APIを実行し、権限エラーとなることを確認
    """
    redmine_url = get_env("REDMINE_URL")
    admin_api_key = get_env("REDMINE_ADMIN_API_KEY")
    user_api_key = get_env("REDMINE_USER_API_KEY")
    project_id = get_env("REDMINE_TEST_PROJECT_ID")
    # 一時ファイルを作成してアップロード
    file_path = create_temp_file()
    upload_result = upload_attachment(
        redmine_url=redmine_url,
        api_key=admin_api_key,
        file_path=file_path,
    )
    assert upload_result["success"] is True
    token = upload_result["token"]
    uploads = [
        {
            "token": token,
            "filename": os.path.basename(file_path),
            "content_type": "application/octet-stream",
        }
    ]
    issue_result = create_issue(
        redmine_url=redmine_url,
        api_key=admin_api_key,
        project_id=project_id,
        subject="permission denied test",
        uploads=uploads,
    )
    attachments = issue_result.get("issue", {}).get("attachments", [])
    assert attachments, "チケット作成時に添付ファイルが登録されていません"
    attachment_id = attachments[0]["id"]
    # 一般ユーザーで削除API実行
    result = delete_attachment(
        redmine_url=redmine_url,
        api_key=user_api_key,
        attachment_id=attachment_id,
    )
    print("permission_denied_result:", result)
    assert result["success"] is False
    # "status_code"が無い場合はerror文字列で判定
    assert "403" in result.get("error", "")
    # ファイル削除
    os.remove(file_path)


def test_delete_attachment_not_found():
    """存在しない添付ファイルID指定時のエラー系テスト"""
    redmine_url = get_env("REDMINE_URL")
    api_key = get_env("REDMINE_USER_API_KEY")
    result = delete_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        attachment_id=999999999,  # 存在しないID
    )
    print("result:", result)
    assert result["success"] is False or result["status_code"] == 404 or "error" in result
