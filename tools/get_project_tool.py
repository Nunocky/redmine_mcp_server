"""Redmineのプロジェクト詳細取得ツール

RedmineAPIClientを利用してプロジェクト詳細を取得する。
"""

from fastmcp.tools.tool import Tool
from tools.redmine_api_client import RedmineAPIClient
from typing import Optional, Dict, Any

def get_project(
    project_id_or_identifier: str,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    include: Optional[str] = None
) -> Dict[str, Any]:
    """Redmineのプロジェクト詳細を取得する

    Args:
        project_id_or_identifier (str): プロジェクトIDまたはidentifier
        redmine_url (str, optional): RedmineサーバーのURL。未指定時は環境変数REDMINE_URLを利用
        api_key (str, optional): RedmineのAPIキー。未指定時は環境変数REDMINE_API_KEYを利用
        include (str, optional): 追加情報（カンマ区切り: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields）

    Returns:
        dict: プロジェクト詳細情報
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    params = {}
    if include:
        params["include"] = include
    endpoint = f"/projects/{project_id_or_identifier}.json"
    resp = client.get(endpoint, params=params)
    resp.raise_for_status()
    return resp.json().get("project", {})

GetProjectTool = Tool.from_function(
    get_project,
    name="get_project",
    description="Redmineのプロジェクト詳細情報を取得します。"
)
