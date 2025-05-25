"""Redmine Attachments API 取得エンドポイントの実機テスト

pytest -s tests/test_main_get_attachment.py
"""

import os
import sys
from pprint import pprint

import pytest
import requests


def test_get_attachment_success():
    """添付ファイル取得APIの正常系テスト

    Args:
        なし

    Raises:
        pytest.fail: 必要な環境変数が未設定の場合

    Notes:
        REDMINE_TEST_ATTACHMENT_ID には事前に存在する添付ファイルIDをセットしてください。
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    attachment_id = os.environ.get("REDMINE_TEST_ATTACHMENT_ID")

    url = f"{redmine_url}/attachments/{attachment_id}.json"
    headers = {"X-Redmine-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        pytest.fail(f"API request failed: status={response.status_code}, body={response.text}")
    result = response.json()
    pprint(result, stream=sys.stderr)
    assert isinstance(result, dict)
    assert "attachment" in result
    attachment = result["attachment"]
    assert "id" in attachment
    assert "filename" in attachment
    assert "content_url" in attachment


def test_get_attachment_not_found():
    """存在しない添付ファイルID指定時のエラー系テスト

    Args:
        なし

    Raises:
        pytest.fail: 必要な環境変数が未設定の場合
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    if not redmine_url or not api_key:
        pytest.fail("REDMINE_URL, REDMINE_USER_API_KEY のいずれかが未設定です")

    url = f"{redmine_url}/attachments/999999999.json"
    headers = {"X-Redmine-API-Key": api_key}
    response = requests.get(url, headers=headers)
    pprint(response.text, stream=sys.stderr)
    assert response.status_code == 404 or response.status_code == 403
