"""Redmineのプロジェクト一覧取得ツール

RedmineAPIClientを利用してプロジェクト一覧を取得する。
"""

from fastmcp.tools.tool import Tool
from tools.redmine_api_client import RedmineAPIClient
from typing import Optional, List, Dict, Any

def get_projects(
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    include: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """Redmineのプロジェクト一覧を取得する

    Args:
        redmine_url (str, optional): RedmineサーバーのURL。未指定時は環境変数REDMINE_URLを利用
        api_key (str, optional): RedmineのAPIキー。未指定時は環境変数REDMINE_API_KEYを利用
        include (str, optional): 追加情報（カンマ区切り: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields）
        limit (int, optional): 取得件数
        offset (int, optional): オフセット

    Returns:
        dict: プロジェクト一覧情報
            - projects (list): プロジェクト情報リスト
            - total_count (int): 総件数
            - limit (int): 取得件数
            - offset (int): オフセット
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    resp = client.get("/projects.json", params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "projects": data.get("projects", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }

GetProjectsTool = Tool.from_function(
    get_projects,
    name="get_projects",
    description="Redmineのプロジェクト一覧を取得します。"
)
