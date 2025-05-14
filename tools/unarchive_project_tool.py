"""Redmineのプロジェクトアーカイブ解除ツール

RedmineAPIClientを利用してプロジェクトのアーカイブを解除する。
"""

from fastmcp.tools.tool import Tool
from tools.redmine_api_client import RedmineAPIClient
from typing import Optional, Dict, Any

def unarchive_project(
    project_id_or_identifier: str,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Redmineのプロジェクトのアーカイブを解除する

    Args:
        project_id_or_identifier (str): プロジェクトIDまたはidentifier
        redmine_url (str, optional): RedmineサーバーのURL
        api_key (str, optional): RedmineのAPIキー

    Returns:
        dict: アーカイブ解除結果（status, message）
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/projects/{project_id_or_identifier}/unarchive.json"
    resp = client.put(endpoint)
    if resp.status_code == 204:
        return {"status": "success", "message": "Project unarchived"}
    else:
        return {"status": "error", "message": resp.text, "status_code": resp.status_code}

UnarchiveProjectTool = Tool.from_function(
    unarchive_project,
    name="unarchive_project",
    description="Redmineのプロジェクトのアーカイブを解除します。"
)
