"""Redmineのプロジェクト作成ツール

RedmineAPIClientを利用して新規プロジェクトを作成する。
"""

from fastmcp.tools.tool import Tool
from tools.redmine_api_client import RedmineAPIClient
from typing import Optional, List, Dict, Any

def create_project(
    name: str,
    identifier: str,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None,
    description: Optional[str] = None,
    homepage: Optional[str] = None,
    is_public: Optional[bool] = None,
    parent_id: Optional[int] = None,
    inherit_members: Optional[bool] = None,
    default_assigned_to_id: Optional[int] = None,
    default_version_id: Optional[int] = None,
    tracker_ids: Optional[List[int]] = None,
    enabled_module_names: Optional[List[str]] = None,
    issue_custom_field_ids: Optional[List[int]] = None,
    custom_field_values: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Redmineの新規プロジェクトを作成する

    Args:
        name (str): プロジェクト名（必須）
        identifier (str): プロジェクト識別子（必須）
        redmine_url (str, optional): RedmineサーバーのURL
        api_key (str, optional): RedmineのAPIキー
        description (str, optional): 説明
        homepage (str, optional): ホームページURL
        is_public (bool, optional): 公開フラグ
        parent_id (int, optional): 親プロジェクトID
        inherit_members (bool, optional): メンバー継承
        default_assigned_to_id (int, optional): デフォルト担当者ID
        default_version_id (int, optional): デフォルトバージョンID
        tracker_ids (List[int], optional): トラッカーIDリスト
        enabled_module_names (List[str], optional): 有効モジュール名リスト
        issue_custom_field_ids (List[int], optional): カスタムフィールドIDリスト
        custom_field_values (Dict[str, Any], optional): カスタムフィールド値

    Returns:
        dict: 作成されたプロジェクト情報またはエラーメッセージ
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    project_data = {
        "name": name,
        "identifier": identifier,
    }
    if description is not None:
        project_data["description"] = description
    if homepage is not None:
        project_data["homepage"] = homepage
    if is_public is not None:
        project_data["is_public"] = is_public
    if parent_id is not None:
        project_data["parent_id"] = parent_id
    if inherit_members is not None:
        project_data["inherit_members"] = inherit_members
    if default_assigned_to_id is not None:
        project_data["default_assigned_to_id"] = default_assigned_to_id
    if default_version_id is not None:
        project_data["default_version_id"] = default_version_id
    if tracker_ids is not None:
        project_data["tracker_ids"] = tracker_ids
    if enabled_module_names is not None:
        project_data["enabled_module_names"] = enabled_module_names
    if issue_custom_field_ids is not None:
        project_data["issue_custom_field_ids"] = issue_custom_field_ids
    if custom_field_values is not None:
        project_data["custom_field_values"] = custom_field_values

    payload = {"project": project_data}
    resp = client.post("/projects.json", json=payload)
    resp.raise_for_status()
    return resp.json().get("project", {})

CreateProjectTool = Tool.from_function(
    create_project,
    name="create_project",
    description="Redmineプロジェクトを作成する"
)
