import requests
from fastmcp.tools.tool import Tool


def get_wiki_pages(redmine_url: str, api_key: str, project_id: str):
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    url = f"{redmine_url.rstrip('/')}/projects/{project_id}/wiki/index.json"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return {
        "wiki_pages": data.get("wiki_pages", []),
    }


GetWikiPagesTool = Tool.from_function(
    get_wiki_pages,
    name="get_wiki_pages",
    description="Get wiki pages from Redmine",
)
