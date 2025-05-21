import os

from tools.redmine_api_client import RedmineAPIClient


def get_wiki_pages(redmine_url: str, api_key: str, project_id: str):
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise ValueError("redmine_url and api_key are required.")
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
