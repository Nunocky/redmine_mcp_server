"""Tool to update a Redmine attachment's meta information (PATCH)"""

from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def update_attachment(
    redmine_url: str,
    api_key: str,
    attachment_id: int,
    update_fields: dict,
    response_format: str = "json",
) -> Dict[str, Any]:
    """
    Update attachment meta information on Redmine.

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        attachment_id (int): Attachment ID
        update_fields (dict): Fields to update
        response_format (str): Response format (default: "json")

    Returns:
        dict: Result of update or error info
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = f"/attachments/{attachment_id}.{response_format}"
    try:
        # Redmine API expects {"attachment": {...}} as body
        body = {"attachment": update_fields}
        resp = client.patch(endpoint=endpoint, json=body)
        success = resp.status_code in (200, 204)
        updated = resp.json().get("attachment") if resp.status_code == 200 else None
        return {
            "success": success,
            "status_code": resp.status_code,
            "updated_attachment": updated,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
