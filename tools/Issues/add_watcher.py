"""Tool to add a watcher to a Redmine issue"""

from tools.redmine_api_client import RedmineAPIClient


def add_watcher(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    user_id: int,
):
    """
    Add a watcher (user_id) to the specified issue (issue_id)

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        issue_id (int): Issue ID
        user_id (int): User ID to add

    Returns:
        dict: Success status and response information
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = f"/issues/{issue_id}/watchers.json"
    data = {"user_id": user_id}
    try:
        resp = client.post(endpoint=endpoint, json=data)
        return {
            "success": resp.status_code in (200, 201, 204),
            "status_code": resp.status_code,
            "response_text": resp.text,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
