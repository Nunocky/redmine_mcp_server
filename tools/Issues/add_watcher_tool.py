"""Redmine課題にウォッチャーを追加するツール"""

import requests
from fastmcp.tools.tool import Tool

def add_watcher(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    user_id: int,
):
    """
    指定した課題(issue_id)にウォッチャー(user_id)を追加する

    Args:
        redmine_url (str): RedmineのベースURL
        api_key (str): APIキー
        issue_id (int): 課題ID
        user_id (int): 追加するユーザーID

    Returns:
        dict: 成功可否とレスポンス情報
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}/watchers.json"
    data = {"user_id": user_id}
    resp = requests.post(url, headers=headers, json=data)
    return {
        "success": resp.status_code in (200, 201, 204),
        "status_code": resp.status_code,
        "response_text": resp.text,
    }

AddWatcherTool = Tool.from_function(
    add_watcher,
    name="add_watcher",
    description="Redmine課題にウォッチャーを追加する"
)
