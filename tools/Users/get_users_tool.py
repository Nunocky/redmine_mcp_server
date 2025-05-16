"""Redmineユーザー一覧取得ツール

Redmineのユーザー一覧を取得するツールです。
"""

from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


class GetUsersTool:
    """Redmineのユーザー一覧取得ツール

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
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[int] = None,
        name: Optional[str] = None,
        group_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """ユーザー一覧を取得する

        Args:
            limit (int, optional): 取得件数
            offset (int, optional): スキップ件数
            status (int, optional): ユーザーステータス（1: アクティブ、2: 登録済み、3: ロック済み）
            name (str, optional): ログイン名、姓名、メールアドレスでフィルタリング
            group_id (int, optional): 特定グループに所属するユーザーでフィルタリング

        Returns:
            dict: ユーザー一覧とページ情報

        Raises:
            Exception: APIリクエスト失敗時
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status is not None:
            params["status"] = status
        if name is not None:
            params["name"] = name
        if group_id is not None:
            params["group_id"] = group_id

        response = self.client.get(
            endpoint="/users.json",
            params=params,
        )
        data = response.json()
        return {
            "users": data.get("users", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
