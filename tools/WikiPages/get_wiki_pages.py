import os
from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_wiki_pages(
    redmine_url: str,
    api_key: str,
    project_id: str,
) -> Dict[str, Any]:
    """Get the list of Redmine project wiki pages.
    Args:
        redmine_url (str): URL of the Redmine server.
        api_key (str): Redmine API key.
        project_id (str): Project ID or identifier.
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    endpoint = f"/projects/{project_id}/wiki/index.json"
    try:
        response = client.get(endpoint=endpoint)
        data = response.json()
        return {
            "wiki_pages": data.get("wiki_pages", []),
        }
    except Exception as e:
        if hasattr(e, "response") and e.response is not None and getattr(e.response, "status_code", None) == 404:
            return {"wiki_pages": []}
        raise
