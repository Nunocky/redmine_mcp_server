"""Redmineのプロジェクトアーカイブツール

RedmineAPIClientを利用してプロジェクトをアーカイブする。
"""

from fastmcp.tools.tool import Tool
from tools.redmine_api_client import RedmineAPIClient
from typing import Optional, Dict, Any

def archive_project(
    project_id_or_identifier: str,
    redmine_url: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Redmineのプロジェクトをアーカイブする

    Args:
        project_id_or_identifier (str): プロジェクトIDまたはidentifier
        redmine_url (str, optional): RedmineサーバーのURL
        api_key (str, optional): RedmineのAPIキー

    Returns:
        dict: アーカイブ結果（status, message）
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/projects/{project_id_or_identifier}/archive.json"
    resp = client.put(endpoint)
    if resp.status_code == 204:
        return {"status": "success", "message": "Project archived"}
    else:
        return {"status": "error", "message": resp.text, "status_code": resp.status_code}

ArchiveProjectTool = Tool.from_function(
    archive_project,
    name="archive_project",
    description="Redmineのプロジェクトをアーカイブします。"
)
