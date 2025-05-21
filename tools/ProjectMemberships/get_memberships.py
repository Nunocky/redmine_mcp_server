"""Redmineのプロジェクトメンバーシップ一覧取得API呼び出し関数

存在しないリソース（404エラー）は空リストを返す。

Returns:
    dict: Membership list and page information

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, Optional

import requests

from tools.redmine_api_client import RedmineAPIClient


def get_memberships(
    redmine_url: str,
    api_key: str,
    project_id: str,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Redmineのプロジェクトメンバーシップ一覧を取得

    Args:
        redmine_url: RedmineサーバのURL
        api_key: Redmine APIキー
        project_id: プロジェクトIDまたは識別子
        offset: スキップする件数
        limit: 取得件数

    Returns:
        dict: メンバーシップ一覧とページ情報
        存在しないリソース（404エラー）は空リストを返す

    Raises:
        Exception: APIリクエスト失敗時（404以外）
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    endpoint = f"/projects/{project_id}/memberships.json"
    try:
        response = client.get(
            endpoint=endpoint,
            params=params,
        )
        data = response.json()
        if "offset" not in data:
            data["offset"] = params.get("offset", 0)
        if "limit" not in data:
            data["limit"] = params.get("limit", 25)
        return data
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"memberships": [], "total_count": 0, "offset": 0, "limit": 0}
        raise
