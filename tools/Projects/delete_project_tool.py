"""Redmineのプロジェクト削除ツール

RedmineAPIClientを利用してプロジェクトを削除する。
"""

from typing import Any, Dict, Optional

import requests
from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def delete_project(
    project_id_or_identifier: str, redmine_url: Optional[str] = None, api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Redmineのプロジェクトを削除する

    Args:
        project_id_or_identifier (str): プロジェクトIDまたはidentifier
        redmine_url (str, optional): RedmineサーバーのURL
        api_key (str, optional): RedmineのAPIキー

    Returns:
        dict: 削除結果（status, message）
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/projects/{project_id_or_identifier}.json"
    try:
        resp = client.delete(endpoint)
        if resp.status_code == 200 or resp.status_code == 204:
            return {"status": "success", "message": "Project deleted"}
        else:
            return {"status": "error", "message": resp.text, "status_code": resp.status_code}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "message": str(e), "status_code": e.response.status_code if hasattr(e, "response") else 500}


DeleteProjectTool = Tool.from_function(delete_project, name="delete_project", description="Redmineプロジェクトを削除する")
