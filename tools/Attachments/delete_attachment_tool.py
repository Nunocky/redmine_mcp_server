"""Tool to delete a Redmine attachment"""

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def delete_attachment(
    redmine_url: str,
    api_key: str,
    attachment_id: int,
    response_format: str = "json",
):
    """
    Delete an attachment from Redmine.

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        attachment_id (int): Attachment ID
        response_format (str): Response format (default: "json")

    Returns:
        dict: Success status and response information
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = f"/attachments/{attachment_id}.{response_format}"
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


DeleteAttachmentTool = Tool.from_function(
    delete_attachment,
    name="delete_attachment",
    description="Deletes an attachment from Redmine.",
)
