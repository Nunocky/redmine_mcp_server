import requests
from fastmcp.tools.tool import Tool

def delete_user(
    redmine_url: str,
    api_key: str,
    user_id: int
):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {
        "X-Redmine-API-Key": api_key
    }
    url = f"{redmine_url.rstrip('/')}/users/{user_id}.json"
    resp = requests.delete(url, headers=headers)
    resp.raise_for_status()
    # Redmineは204 No Contentを返す
    return {"deleted": True}

DeleteUserTool = Tool.from_function(
    delete_user,
    name="delete_user",
    description="Delete a user in Redmine by user_id."
)
