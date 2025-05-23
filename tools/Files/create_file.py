import requests

from tools.redmine_api_client import RedmineAPIClient


def create_file(
    redmine_url: str,
    api_key: str,
    project_id: str,
    file: dict,
):
    """Create a new file for a Redmine project.

    Args:
        redmine_url (str): Redmine server URL.
        api_key (str): Redmine API key.
        project_id (str): Project ID or identifier.
        file (dict): {
            "token": str,  # required
            "version_id": int,  # optional
            "filename": str,  # optional
            "description": str,  # optional
        }

    Returns:
        dict: 登録したファイル情報

    Raises:
        Exception: If API request fails.
    """
    if "token" not in file or not file["token"]:
        raise ValueError("file['token'] is required (from /uploads API)")

    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    payload = {"file": file}
    try:
        response = client.post(
            endpoint=f"/projects/{project_id}/files.json",
            json=payload,
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise
