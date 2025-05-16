import requests
from fastmcp.tools.tool import Tool

def get_user(redmine_url: str, api_key: str, user_id: int, include: str = None):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
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
    description="Get details of a user from Redmine by user_id."
)
