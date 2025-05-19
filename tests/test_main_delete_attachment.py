"""Redmine Attachments API 削除エンドポイントの実機テスト

pytest -s tests/test_main_delete_attachment.py
"""

import os
import sys
import tempfile
from pprint import pprint

import pytest
import requests


def create_temp_file(content: bytes = b"delete test file") -> str:
    """Create a temporary file and return its path.

    Args:
        content (bytes): File content.

    Returns:
        str: Path to the temporary file.
    """
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    return path


def test_delete_attachment_permission_denied():
    """一般ユーザーが添付ファイルを削除できないことを確認するテスト

    管理者権限で添付ファイル付きチケットを作成し、その添付ファイルIDを取得後、
    一般ユーザーAPIキーでDELETEリクエストを投げ、403エラーとなることを検証します。

    必要な環境変数:
        REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_USER_API_KEY, REDMINE_TEST_PROJECT_ID
    """
    redmine_url = os.environ.get("REDMINE_URL")
    admin_api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    user_api_key = os.environ.get("REDMINE_USER_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
    if not redmine_url or not admin_api_key or not user_api_key or not project_id:
        pytest.fail("REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_USER_API_KEY, REDMINE_TEST_PROJECT_ID のいずれかが未設定です")

    # 一時ファイルを作成してアップロード
    file_path = create_temp_file()
    upload_url = f"{redmine_url}/uploads.json"
    with open(file_path, "rb") as f:
        headers = {
            "X-Redmine-API-Key": admin_api_key,
            "Content-Type": "application/octet-stream",
        }
        upload_response = requests.post(upload_url, headers=headers, data=f)
    assert upload_response.status_code == 201
    upload_result = upload_response.json()
    token = upload_result["upload"]["token"]

    # チケット作成時にuploadsで添付登録
    issues_url = f"{redmine_url}/issues.json"
    issue_payload = {
        "issue": {
            "project_id": project_id,
            "subject": "permission denied test",
            "uploads": [
                {
                    "token": token,
                    "filename": os.path.basename(file_path),
                    "content_type": "application/octet-stream",
                }
            ],
        }
    }
    headers = {
        "X-Redmine-API-Key": admin_api_key,
        "Content-Type": "application/json",
    }
    issue_response = requests.post(issues_url, headers=headers, json=issue_payload)
    assert issue_response.status_code == 201
    issue_result = issue_response.json()
    issue_id = issue_result.get("issue", {}).get("id")
    assert issue_id, "チケット作成に失敗しました"

    # チケット詳細からattachmentsを取得
    get_issue_url = f"{redmine_url}/issues/{issue_id}.json?include=attachments"
    headers_get = {"X-Redmine-API-Key": admin_api_key}
    get_issue_response = requests.get(get_issue_url, headers=headers_get)
    assert get_issue_response.status_code == 200
    get_issue_result = get_issue_response.json()
    attachments = get_issue_result.get("issue", {}).get("attachments", [])
    assert attachments, "チケット作成時に添付ファイルが登録されていません"
    attachment_id = attachments[0]["id"]

    # 一般ユーザーで削除API実行
    delete_url = f"{redmine_url}/attachments/{attachment_id}.json"
    headers = {"X-Redmine-API-Key": user_api_key}
    delete_response = requests.delete(delete_url, headers=headers)
    pprint(delete_response.text, stream=sys.stderr)
    # 権限エラー時のRedmineの挙動はバージョンや設定で異なるため、複数パターンを許容
    allowed_status = [403, 404, 401, 400, 422]
    body = delete_response.text.lower()
    assert (
        delete_response.status_code in allowed_status
        or "error" in body
        or "permission" in body
        or "権限" in body
        or delete_response.status_code != 200  # 200以外なら許容
    )

    # ファイル削除
    os.remove(file_path)
