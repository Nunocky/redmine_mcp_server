import requests
from fastmcp.tools.tool import Tool


def create_user(
    redmine_url: str,
    api_key: str,
    login: str,
    firstname: str,
    lastname: str,
    mail: str,
    password: str = None,
    auth_source_id: int = None,
    mail_notification: str = None,
    must_change_passwd: bool = None,
    generate_password: bool = None,
    custom_fields: list = None,
    send_information: bool = None,
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": "application/json"}
    user_data = {"login": login, "firstname": firstname, "lastname": lastname, "mail": mail}
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

    url = f"{redmine_url.rstrip('/')}/users.json"
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()


CreateUserTool = Tool.from_function(create_user, name="create_user", description="Create a new user in Redmine.")
