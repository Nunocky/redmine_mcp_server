from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_issue_relations(
    redmine_url: str,
    api_key: str,
    issue_id: int = None,
    limit: int = None,
    offset: int = None,
) -> Dict[str, Any]:
    """Get a list of Redmine issue relations
    Args:
        redmine_url (str): URL of the Redmine server.
        api_key (str): Redmine API key.
        issue_id (int, optional): ID of the issue to get relations for. If None, retrieves all relations.
        limit (int, optional): Number of records to retrieve. Defaults to 25 if not specified.
        offset (int, optional): Number of records to skip. Defaults to 0 if not specified.
    Returns:
        Dict[str, Any]: A dictionary containing the relations and pagination information.
        - "relations": List of relations.
        - "total_count": Total number of relations.
        - "limit": Limit used for pagination.
        - "offset": Offset used for pagination.
        - "error": Error message if an error occurs.
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
