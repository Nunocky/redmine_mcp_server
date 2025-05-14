"""課題一覧取得ツール

Redmineの課題（Issues）を一覧取得するツールです。

Returns:
    dict: 課題一覧とページ情報

Raises:
    Exception: APIリクエスト失敗時
"""

from typing import Any, Dict, Optional
from tools.redmine_api_client import RedmineAPIClient


class GetIssuesTool:
    """Redmineの課題一覧取得ツール

    Attributes:
        client (RedmineAPIClient): Redmine APIクライアント
    """

    def __init__(self, client: Optional[RedmineAPIClient] = None) -> None:
        """コンストラクタ

        Args:
            client (RedmineAPIClient, optional): APIクライアント。未指定時は新規生成。
        """
        self.client = client or RedmineAPIClient()

    def run(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        include: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """課題一覧を取得する

        Args:
            offset (int, optional): スキップする件数
            limit (int, optional): 取得件数
            sort (str, optional): ソートカラム（例: 'updated_on:desc'）
            include (str, optional): 追加情報（カンマ区切り）
            filters (dict, optional): その他のフィルタ条件

        Returns:
            dict: 課題一覧とページ情報

        Raises:
            Exception: APIリクエスト失敗時
        """
        params: Dict[str, Any] = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if sort is not None:
            params["sort"] = sort
        if include is not None:
            params["include"] = include
        if filters:
            params.update(filters)

        response = self.client.get(
            endpoint="/issues.json",
            params=params,
        )
        return response.json()
