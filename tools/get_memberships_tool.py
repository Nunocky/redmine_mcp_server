"""Redmineプロジェクトメンバーシップ一覧取得ツール

Redmineのプロジェクトメンバーシップ一覧を取得するツールです。
"""

from typing import Any, Dict, Optional

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_memberships(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    project_id: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    """プロジェクトメンバーシップ一覧を取得する

    Args:
        redmine_url (str): RedmineサーバーのURL
        api_key (str): RedmineのAPIキー
        project_id (str): プロジェクトID
        limit (int, optional): 取得件数
        offset (int, optional): スキップ件数

    Returns:
        dict: メンバーシップ一覧とページ情報

    Raises:
        Exception: APIリクエスト失敗時
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset

    endpoint = f"/projects/{project_id}/memberships.json"
    response = client.get(
        endpoint=endpoint,
        params=params,
    )
    data = response.json()
    return {
        "memberships": data.get("memberships", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetMembershipsTool = Tool.from_function(
    get_memberships,
    name="get_projects",
    description="Redmineプロジェクトメンバーシップ一覧を取得する",
)
