"""Attachments API update_attachment 実機テスト

pytest -s tests/Attachments/test_update_attachment_tool.py
"""

import os
import tempfile

import pytest

from tools.Attachments.update_attachment_tool import update_attachment
from tools.Attachments.upload_attachment_tool import upload_attachment
from tools.Issues.create_issue_tool import create_issue


def create_temp_file(content: bytes = b"update test file") -> str:
    """一時ファイルを作成しパスを返す"""
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    return path


@pytest.mark.skip(reason="PATCH API is not documented yet.")
def test_update_attachment_success():
    """添付ファイル情報更新APIの正常系テスト（事前にアップロード＆チケット登録）"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    project_id = os.environ.get("REDMINE_TEST_PROJECT_ID")
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
        }
    ]
    issue_result = create_issue(
        redmine_url=redmine_url,
        api_key=api_key,
        project_id=project_id,
        subject="update attachment test",
        uploads=uploads,
    )
    print("issue_result:", issue_result)
    issue_id = issue_result.get("issue", {}).get("id")
    from tools.Issues.get_issue_tool import get_issue

    get_issue_result = get_issue(
        issue_id=issue_id,
        redmine_url=redmine_url,
        api_key=api_key,
        include="attachments",
    )
    print("get_issue_result:", get_issue_result)
    attachments = get_issue_result.get("issue", {}).get("attachments", [])
    assert attachments, "チケット作成時に添付ファイルが登録されていません"
    attachment_id = attachments[0]["id"]
    # 更新API実行
    update_fields = {"description": "updated by test"}
    result = update_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        attachment_id=attachment_id,
        update_fields=update_fields,
    )
    print("update_result:", result)
    if not result["success"]:
        pytest.fail(f"update_attachment failed: {result}")
    assert result["status_code"] in (200, 204)
    if result["updated_attachment"] is not None:
        assert result["updated_attachment"].get("description") == "updated by test"
    # ファイル削除
    os.remove(file_path)


@pytest.mark.skip(reason="PATCH API is not documented yet.")
def test_update_attachment_not_found():
    """存在しない添付ファイルID指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    update_fields = {"description": "should not update"}
    result = update_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        attachment_id=999999999,  # 存在しないID
        update_fields=update_fields,
    )
    print("result:", result)
    assert result["success"] is False or result["status_code"] == 404 or "error" in result
