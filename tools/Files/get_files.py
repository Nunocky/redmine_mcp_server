import requests

from tools.redmine_api_client import RedmineAPIClient


def get_files(
    redmine_url: str,
    api_key: str,
    project_id: str,
):
    """Get files for a Redmine project.

    Args:
        redmine_url (str): Redmine server URL.
        api_key (str): Redmine API key.
        project_id (str): Project ID or identifier.

    Returns:
        dict: {"files": [...]} or {"files": []} if not found.

    Raises:
        Exception: If API request fails (except 404).
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    try:
        response = client.get(
            endpoint=f"/projects/{project_id}/files.json",
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"files": []}
        raise
