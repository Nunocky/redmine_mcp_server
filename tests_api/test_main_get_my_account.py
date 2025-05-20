"""test_main_get_my_account.py

/my/account エンドポイントにアクセスし、アカウント情報(JSON)を取得する統合テスト。

- .env から BASE_URL, API_KEY を取得
- /my/account に GET リクエスト
- ステータスコードとJSON構造を検証

GoogleスタイルDocstring、PEP8準拠
"""

import os

import pytest
import requests


def _get_base_url_and_api_key():
    """Load BASE_URL and API_KEY from .env file.

    Returns:
        tuple: (base_url, api_key)
    """
    base_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_USER_API_KEY")
    if not base_url or not api_key:
        raise RuntimeError("REDMINE_URL and REDMINE_USER_API_KEY must be set in .env")
    return base_url, api_key


def test_get_my_account():
    """Test /my/account endpoint returns valid account info as JSON.

    Raises:
        AssertionError: If response is not as expected.
    """
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")

    url = f"{redmine_url}/my/account.json"
    headers = {"X-Redmine-API-Key": api_key}
    response = requests.get(url, headers=headers)

    assert response.status_code == 200
    result = response.json()
    print(result)
    # Check JSON structure
    assert isinstance(result, dict)
    assert "user" in result
    user_info = result["user"]
    assert "id" in user_info
    assert "login" in user_info
    assert "firstname" in user_info
    assert "lastname" in user_info
    assert "mail" in user_info


def test_get_my_account_invalid_key():
    """Test /my/account endpoint with invalid API key returns 401."""
    base_url, _ = _get_base_url_and_api_key()
    url = f"{base_url}/my/account.json"
    headers = {"X-Redmine-API-Key": "invalid_key"}
    response = requests.get(url, headers=headers)
    if "text/html" in response.headers.get("Content-Type", ""):
        pytest.skip("RedmineがHTMLを返しました。APIが有効か、APIキー・Redmine設定を確認してください。")
    # Redmineのバージョンや設定によっては200でエラーメッセージを返す場合もある
    if response.status_code == 401:
        return
    # 200の場合はbodyに"Invalid API key"等が含まれるか確認
    if "Invalid API key" in response.text or "APIキー" in response.text:
        return
    pytest.fail(f"無効なAPIキーで401やエラーが返りませんでした: status={response.status_code}, body={response.text[:200]}")
