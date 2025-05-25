"""
Query Tool
保存済み検索条件
"""

from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_queries(
    redmine_url: str,
    api_key: str,
) -> Dict[str, Any]:
    """Get the list of saved queries in Redmine.

    Args:
        redmine_url (str): URL of the Redmine server.
        api_key (str): Redmine API key.
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
    try:
        response = client.get(endpoint="/queries.json")
        data = response.json()
        return {
            "queries": data.get("queries", []),
        }
    except Exception as e:
        if hasattr(e, "response") and e.response is not None and getattr(e.response, "status_code", None) == 404:
            return {"queries": []}
        raise
