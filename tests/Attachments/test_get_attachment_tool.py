"""Attachments API get_attachment 実機テスト

pytest -s tests/Attachments/test_get_attachment_tool.py
"""

import os

from tools.Attachments.get_attachment_tool import get_attachment


def test_get_attachment_success():
    """添付ファイル取得APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    # 添付ファイルIDは事前に存在するものを指定してください
    attachment_id = os.environ.get("REDMINE_TEST_ATTACHMENT_ID")
    result = get_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        attachment_id=int(attachment_id),
    )
    print("result:", result)
    assert result["success"] is True
    assert "filename" in result
    assert "content_url" in result


def test_get_attachment_not_found():
    """存在しない添付ファイルID指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    result = get_attachment(
        redmine_url=redmine_url,
        api_key=api_key,
        attachment_id=999999999,  # 存在しないID
    )
    print("result:", result)
    assert result["success"] is False
    assert "error" in result
