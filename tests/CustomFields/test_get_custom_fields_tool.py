import os

import pytest
import requests

from tools.CustomFields.get_custom_fields import get_custom_fields


def test_get_custom_fields_success():
    """管理者APIキーでカスタムフィールド一覧が取得できること"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_ADMIN_API_KEY"]
    result = get_custom_fields(redmine_url, api_key)
    assert "custom_fields" in result
    assert isinstance(result["custom_fields"], list)


def test_get_custom_fields_invalid_key():
    """不正なAPIキーの場合に認証エラーとなること"""
    redmine_url = os.environ.get("REDMINE_URL", "http://localhost:9999")
    api_key = "invalid_key"
    with pytest.raises(requests.exceptions.HTTPError):
        get_custom_fields(redmine_url, api_key)
