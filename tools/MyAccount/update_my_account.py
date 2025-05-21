"""UpdateMyAccountTool: PUT /my/account を実行するツール

- ログインユーザー自身のアカウント情報を更新する
- 更新可能項目: firstname, lastname, mail, custom_fields
"""

from typing import Any, Dict, List, Optional

from tools.redmine_api_client import RedmineAPIClient


def update_my_account(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    mail: Optional[str] = None,
    custom_fields: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Update the current user's account information using RedmineApiClient.

    Args:
        base_url (str, optional): Redmine server base URL
        api_key (str, optional): Redmine API key
        firstname (str, optional): First name of the user
        lastname (str, optional): Last name of the user
        mail (str, optional): Email address of the user
        custom_fields (list[dict], optional): Custom fields to update

    Returns:
        dict: Updated user account information

    Raises:
        Exception: If the API request fails or response is invalid
    """
    client = RedmineAPIClient(base_url=base_url, api_key=api_key)
    endpoint = "/my/account.json"
    data = {
        "user": {
            "firstname": firstname,
            "lastname": lastname,
            "mail": mail,
            "custom_fields": custom_fields,
        }
    }
    try:
        response = client.put(endpoint, json=data)
        data = response.json()
        return data
    except Exception as e:
        raise Exception(f"Failed to update account info: {e}")
