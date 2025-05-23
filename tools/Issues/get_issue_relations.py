from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_issue_relations(
    redmine_url: str,
    api_key: str,
    issue_id: int = None,
    limit: int = None,
    offset: int = None,
) -> Dict[str, Any]:
    """
    Get a list of Redmine issue relations
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if issue_id:
        endpoint = f"/issues/{issue_id}/relations.json"
    else:
        endpoint = "/relations.json"
    try:
        resp = client.get(
            endpoint=endpoint,
            params=params,
        )
        data = resp.json()
        return {
            "relations": data.get("relations", []),
            "total_count": data.get("total_count", 0),
            "limit": data.get("limit", limit if limit is not None else 25),
            "offset": data.get("offset", offset if offset is not None else 0),
        }
    except Exception as e:
        return {
            "relations": [],
            "total_count": 0,
            "limit": limit if limit is not None else 25,
            "offset": offset if offset is not None else 0,
            "error": str(e),
        }
