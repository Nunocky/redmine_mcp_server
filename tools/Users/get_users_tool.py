"""Redmine User List Retrieval Tool

RedmineAPIClient を利用してユーザー一覧を取得します。
"""

from typing import Any, Dict, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_users(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    status: Optional[int] = None,
    name: Optional[str] = None,
    group_id: Optional[int] = None,
) -> Dict[str, Any]:
    """Redmineのユーザー一覧を取得

    Args:
        redmine_url (str, optional): RedmineサーバーのURL。指定しない場合は環境変数 REDMINE_URL を利用
        api_key (str, optional): Redmine APIキー。指定しない場合は環境変数 REDMINE_ADMIN_API_KEY を利用
        limit (int, optional): 取得件数
        offset (int, optional): スキップ件数
        status (int, optional): ユーザーステータス (1: active, 2: registered, 3: locked)
        name (str, optional): ログイン名、氏名、メールアドレスでフィルタ
        group_id (int, optional): 指定グループに所属するユーザーでフィルタ

    Returns:
        dict: ユーザー一覧情報
            - users (list): ユーザー情報リスト
            - total_count (int): 総件数
            - limit (int): 取得件数
            - offset (int): オフセット
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
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
    resp = client.get("/users.json", params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "users": data.get("users", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetUsersTool = Tool.from_function(
    get_users,
    name="get_users",
    description="Redmineのユーザー一覧を取得する",
)
