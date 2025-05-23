"""
Query Tool
保存済み検索条件
"""

import os
from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_queries(
    redmine_url: str,
    api_key: str,
) -> Dict[str, Any]:
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise ValueError("redmine_url and api_key are required.")
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
