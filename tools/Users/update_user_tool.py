import requests
from fastmcp.tools.tool import Tool

def update_user(
    redmine_url: str,
    api_key: str,
    user_id: int,
    login: str = None,
    firstname: str = None,
    lastname: str = None,
    mail: str = None,
    password: str = None,
    auth_source_id: int = None,
    mail_notification: str = None,
    must_change_passwd: bool = None,
    generate_password: bool = None,
    custom_fields: list = None,
    admin: bool = None
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {
        "X-Redmine-API-Key": api_key,
        "Content-Type": "application/json"
    }
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
    url = f"{redmine_url.rstrip('/')}/users/{user_id}.json"
    resp = requests.put(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json() if resp.content else {}

UpdateUserTool = Tool.from_function(
    update_user,
    name="update_user",
    description="Update a user in Redmine by user_id."
)
