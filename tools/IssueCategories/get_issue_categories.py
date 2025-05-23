import requests

from tools.redmine_api_client import RedmineAPIClient


def get_issue_categories(
    redmine_url: str,
    api_key: str,
    project_id: str,
):
    """Get issue categories for a Redmine project.

    Args:
        redmine_url (str): Redmine server URL.
        api_key (str): Redmine API key.
        project_id (str): Project ID or identifier.

    Returns:
        dict: Issue categories list (API response as is). If not found, returns empty list.

    Raises:
        Exception: If API request fails (except 404).
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    try:
        response = client.get(
            endpoint=f"/projects/{project_id}/issue_categories.json",
        )
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"issue_categories": []}
        raise
