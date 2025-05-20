"""Tool to remove a watcher from a Redmine issue"""

from tools.redmine_api_client import RedmineAPIClient


def remove_watcher(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    user_id: int,
):
    """
    Remove a watcher (user_id) from the specified issue (issue_id)

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        issue_id (int): Issue ID
        user_id (int): User ID to remove

    Returns:
        dict: Success status and response information
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = f"/issues/{issue_id}/watchers/{user_id}.json"
    try:
        resp = client.delete(endpoint=endpoint)
        return {
            "success": resp.status_code in (200, 204),
            "status_code": resp.status_code,
            "response_text": resp.text,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
