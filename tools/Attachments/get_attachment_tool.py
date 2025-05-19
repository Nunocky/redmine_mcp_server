"""Tool to get a Redmine attachment's meta information"""

from fastmcp.tools.tool import Tool

from tools.redmine_api_client import RedmineAPIClient


def get_attachment(
    redmine_url: str,
    api_key: str,
    attachment_id: int,
    response_format: str = "json",
):
    """
    Get attachment meta information from Redmine.

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        attachment_id (int): Attachment ID
        response_format (str): Response format (default: "json")

    Returns:
        dict: Attachment meta information or error info
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = f"/attachments/{attachment_id}.{response_format}"
    try:
        resp = client.get(endpoint=endpoint)
        data = resp.json()["attachment"]
        return {
            "success": True,
            "id": data["id"],
            "filename": data["filename"],
            "filesize": data["filesize"],
            "content_type": data["content_type"],
            "description": data.get("description"),
            "content_url": data["content_url"],
            "author": data["author"],
            "created_on": data["created_on"],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


GetAttachmentTool = Tool.from_function(
    get_attachment,
    name="get_attachment",
    description="Retrieves Redmine attachment information.",
)
