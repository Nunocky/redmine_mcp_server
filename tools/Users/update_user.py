"""Redmine User Update Tool

Update user information using RedmineAPIClient.
If 204 No Content is returned, fetch and return the latest information with GET. Raise Exception for 404 or other errors.

Returns:
    dict: Updated user information

Raises:
    Exception: When API request fails (including 404 errors)
"""

from typing import Any, Dict, List, Optional

from tools.redmine_api_client import RedmineAPIClient


def update_user(
    redmine_url: str,
    api_key: str,
    user_id: int,
    login: Optional[str] = None,
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    mail: Optional[str] = None,
    password: Optional[str] = None,
    auth_source_id: Optional[int] = None,
    mail_notification: Optional[str] = None,
    must_change_passwd: Optional[bool] = None,
    generate_password: Optional[bool] = None,
    custom_fields: Optional[List[Any]] = None,
    admin: Optional[bool] = None,
) -> Dict[str, Any]:
    """Update a user in Redmine by user_id

    Args:
        redmine_url: URL of the Redmine server
        api_key: Redmine API key
        user_id: User ID to update
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
        admin: Admin flag

    Returns:
        dict: Updated user information

    Raises:
        Exception: When API request fails (including 404 errors)
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    user_data = {}
    if login is not None:
        user_data["login"] = login
    if firstname is not None:
        user_data["firstname"] = firstname
    if lastname is not None:
        user_data["lastname"] = lastname
    if mail is not None:
        user_data["mail"] = mail
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
    if admin is not None:
        user_data["admin"] = admin

    payload = {"user": user_data}
    endpoint = f"/users/{user_id}.json"
    resp = client.put(endpoint, json=payload)
    if resp.status_code == 204:
        # 更新後の最新情報を取得して返す
        get_resp = client.get(endpoint)
        get_resp.raise_for_status()
        return get_resp.json().get("user", {})
    resp.raise_for_status()
    return resp.json().get("user", {})
