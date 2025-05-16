import os

import requests
from fastmcp.tools.tool import Tool


def get_queries(
    redmine_url: str,
    api_key: str,
):
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    url = f"{redmine_url.rstrip('/')}/queries.json"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return {
        "queries": data.get("queries", []),
    }


GetQueriesTool = Tool.from_function(
    get_queries,
    name="get_queries",
    description="Get a list of queries from Redmine.",
)
