from typing import Optional, Union

import requests
from fastmcp.tools.tool import Tool


def get_user(
    redmine_url: str,
    api_key: str,
    user_id: Union[int, str],
    include: Optional[str] = None,
):
    """Redmineユーザー詳細を取得

    Args:
        redmine_url (str): RedmineのURL
        api_key (str): Redmine API キー
        user_id (Union[int, str]): ユーザーID または 'current' (現在のユーザー)
        include (Optional[str], optional): レスポンスに含める関連情報（memberships, groups）

    Returns:
        Dict[str, Any]: ユーザー詳細情報

    Raises:
        requests.exceptions.HTTPError: APIリクエスト失敗時
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if include:
        params["include"] = include
    url = f"{redmine_url.rstrip('/')}/users/{user_id}.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()


GetUserTool = Tool.from_function(
    get_user,
    name="get_user",
    description="Redmineユーザー詳細を取得",
)
