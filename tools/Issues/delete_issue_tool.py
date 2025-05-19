from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def delete_issue(redmine_url: str, api_key: str, issue_id: int):
    """
    Delete an issue from Redmine.

    Args:
        redmine_url (str): Redmine base URL
        api_key (str): API key
        issue_id (int): Issue ID

    Returns:
        dict: Success status and response information
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = f"/issues/{issue_id}.json"
    try:
        resp = client.delete(endpoint=endpoint)
        return {"success": resp.status_code in (200, 204), "status_code": resp.status_code, "response_text": resp.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


DeleteIssueTool = Tool.from_function(delete_issue, name="delete_issue", description="Delete an issue from Redmine.")
