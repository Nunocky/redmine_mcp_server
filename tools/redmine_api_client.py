"""Redmine APIクライアント

RedmineのREST APIへの共通アクセス処理を提供するクラス。
"""

import os
from typing import Any, Dict, Optional, Union

import requests


class RedmineAPIClient:
    """Redmine APIクライアント

    Attributes:
        base_url (str): RedmineサーバーのベースURL
        api_key (str): RedmineのAPIキー
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """初期化

        Args:
            base_url (str, optional): RedmineサーバーのベースURL
            api_key (str, optional): RedmineのAPIキー
        """
        self.base_url = base_url or os.environ.get("REDMINE_URL")
        self.api_key = api_key or os.environ.get("REDMINE_ADMIN_API_KEY")
        if not self.base_url or not self.api_key:
            raise ValueError("RedmineのURLまたはAPIキーが設定されていません。")

    def _headers(self) -> Dict[str, str]:
        """APIリクエスト用ヘッダーを生成

        Returns:
            dict: ヘッダー情報
        """
        return {"X-Redmine-API-Key": self.api_key}

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        """APIリクエストを送信

        Args:
            method (str): HTTPメソッド
            endpoint (str): エンドポイントパス（例: '/projects.json'）
            params (dict, optional): クエリパラメータ
            data (dict or str, optional): POST/PUTデータ
            json (dict, optional): JSONデータ
            headers (dict, optional): 追加ヘッダー

        Returns:
            requests.Response: レスポンスオブジェクト

        Raises:
            requests.HTTPError: HTTPエラー時
        """
        url = self.base_url.rstrip("/") + endpoint
        req_headers = self._headers()
        if headers:
            req_headers.update(headers)
        resp = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=req_headers,
        )
        resp.raise_for_status()
        return resp

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """GETリクエスト

        Args:
            endpoint (str): エンドポイントパス
            params (dict, optional): クエリパラメータ

        Returns:
            requests.Response: レスポンス
        """
        return self._request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """POSTリクエスト

        Args:
            endpoint (str): エンドポイントパス
            data (dict, optional): フォームデータ
            json (dict, optional): JSONデータ

        Returns:
            requests.Response: レスポンス
        """
        return self._request("POST", endpoint, data=data, json=json)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """PUTリクエスト

        Args:
            endpoint (str): エンドポイントパス
            data (dict, optional): フォームデータ
            json (dict, optional): JSONデータ

        Returns:
            requests.Response: レスポンス
        """
        return self._request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint: str) -> requests.Response:
        """DELETEリクエスト

        Args:
            endpoint (str): エンドポイントパス

        Returns:
            requests.Response: レスポンス
        """
        return self._request("DELETE", endpoint)
