"""Tool to upload a file as a Redmine attachment (uploads API)

Redmine REST API: POST /uploads.json
Content-Type: application/octet-stream
"""

from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def upload_attachment(
    redmine_url: str,
    api_key: str,
    file_path: str,
    content_type: str = "application/octet-stream",
) -> Dict[str, Any]:
    """Upload a file to Redmine as an attachment.

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        file_path (str): Path to the file to upload
        content_type (str): MIME type (default: application/octet-stream)

    Returns:
        dict: upload token and response info
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    endpoint = "/uploads.json"
    try:
        with open(file_path, "rb") as f:
            headers = client._headers()
            headers.update(
                {
                    "Content-Type": content_type,
                    "Accept": "*/*",
                }
            )
            resp = client._request(
                method="POST",
                endpoint=endpoint,
                data=f.read(),
                headers=headers,
            )
        data = resp.json()
        return {
            "success": True,
            "token": data.get("upload", {}).get("token"),
            "response": data,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
