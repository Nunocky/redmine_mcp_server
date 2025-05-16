"""Redmine課題詳細取得ツール"""

import requests
from fastmcp.tools.tool import Tool

def get_issue(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    include: str = None,
):
    """
    指定した課題(issue_id)の詳細情報を取得する

    Args:
        redmine_url (str): RedmineのベースURL
        api_key (str): APIキー
        issue_id (int): 課題ID
        include (str, optional): 追加情報（カンマ区切り）

    Returns:
        dict: 課題詳細情報
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if include:
        params["include"] = include
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

GetIssueTool = Tool.from_function(
    get_issue,
    name="get_issue",
    description="Redmine課題情報を取得する"
)
