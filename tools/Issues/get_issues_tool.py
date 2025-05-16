"""課題一覧取得ツール

Redmineの課題（Issues）を一覧取得するツールです。
存在しないリソース（404エラー）の場合は空の結果を返します。

Returns:
    dict: 課題一覧とページ情報

Raises:
    Exception: APIリクエスト失敗時（404エラーを除く）
"""

from typing import Any, Dict, Optional

import requests
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
        存在しないリソース（404エラー）の場合は空の結果を返します

    Raises:
        Exception: APIリクエスト失敗時（404エラーを除く）
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

    try:
        response = client.get(
            endpoint="/issues.json",
            params=params,
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        # 404エラーの場合は空の結果を返す
        if e.response.status_code == 404:
            return {"issues": [], "total_count": 0, "offset": 0, "limit": 0}
        # その他のエラーは再度発生させる
        raise


GetIssuesTool = Tool.from_function(
    get_issues,
    name="get_issues",
    description="Redmineの課題一覧を取得します",
)
