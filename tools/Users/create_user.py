"""Redmine User Creation Tool

Create a new user using RedmineAPIClient.
404エラー時は空dict、他エラーは例外送出。

Returns:
    dict: APIレスポンスそのまま（userキー含む場合も含まない場合も）

Raises:
    Exception: When API request fails (excluding 404 errors)
"""

from typing import Any, Dict, List, Optional

import requests

from tools.redmine_api_client import RedmineAPIClient


def create_user(
    redmine_url: str,
    api_key: str,
    login: str,
    firstname: str,
    lastname: str,
    mail: str,
    password: Optional[str] = None,
    auth_source_id: Optional[int] = None,
    mail_notification: Optional[str] = None,
    must_change_passwd: Optional[bool] = None,
    generate_password: Optional[bool] = None,
    custom_fields: Optional[List[Any]] = None,
    send_information: Optional[bool] = None,
) -> Dict[str, Any]:
    """Create a new user in Redmine

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        login: User login
        firstname: First name
        lastname: Last name
        mail: Email address
        password: Password
        auth_source_id: Auth source ID
        mail_notification: Mail notification setting
        must_change_passwd: Must change password flag
        generate_password: Generate password flag
        custom_fields: Custom fields
        send_information: Send information flag

    Returns:
        APIレスポンスそのまま（userキー含む場合も含まない場合も）

    Raises:
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    user_data = {
        "login": login,
        "firstname": firstname,
        "lastname": lastname,
        "mail": mail,
    }
    if password is not None:
        user_data["password"] = password
    if auth_source_id is not None:
        user_data["auth_source_id"] = auth_source_id
    if mail_notification is not None:
        user_data["mail_notification"] = mail_notification
    if must_change_passwd is not None:
        user_data["must_change_passwd"] = must_change_passwd
    if generate_password is not None:
        user_data["generate_password"] = generate_password
    if custom_fields is not None:
        user_data["custom_fields"] = custom_fields

    payload = {"user": user_data}
    if send_information is not None:
        payload["send_information"] = send_information

    try:
        resp = client.post("/users.json", json=payload)
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {}
        raise
