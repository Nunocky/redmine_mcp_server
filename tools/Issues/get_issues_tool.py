"""課題一覧取得ツール

Redmineの課題（Issues）を一覧取得するツールです。

Returns:
    dict: 課題一覧とページ情報

Raises:
    Exception: APIリクエスト失敗時
"""

from typing import Any, Dict, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_issues(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    sort: Optional[str] = None,
    include: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Redmineの課題一覧を取得する

    Args:
        offset: スキップする件数
        limit: 取得件数
        sort: ソートカラム（例: 'updated_on:desc'）
        include: 追加情報（カンマ区切り）
        filters: その他のフィルタ条件

    Returns:
        課題一覧とページ情報

    Raises:
        Exception: APIリクエスト失敗時
    """
    # 直接RedmineAPIClientを使ってAPIを呼び出す
    client = RedmineAPIClient()
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

    response = client.get(
        endpoint="/issues.json",
        params=params,
    )
    return response.json()


GetIssuesTool = Tool.from_function(
    get_issues,
    name="get_issues",
    description="Redmineの課題一覧を取得する",
)
