"""Redmine課題からウォッチャーを削除するツール"""

import requests
from fastmcp.tools.tool import Tool

def remove_watcher(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    user_id: int,
):
    """
    指定した課題(issue_id)からウォッチャー(user_id)を削除する

    Args:
        redmine_url (str): RedmineのベースURL
        api_key (str): APIキー
        issue_id (int): 課題ID
        user_id (int): 削除するユーザーID

    Returns:
        dict: 成功可否とレスポンス情報
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}/watchers/{user_id}.json"
    resp = requests.delete(url, headers=headers)
    return {
        "success": resp.status_code in (200, 204),
        "status_code": resp.status_code,
        "response_text": resp.text,
    }

RemoveWatcherTool = Tool.from_function(
    remove_watcher,
    name="remove_watcher",
    description="Redmine課題からウォッチャーを削除する"
)
