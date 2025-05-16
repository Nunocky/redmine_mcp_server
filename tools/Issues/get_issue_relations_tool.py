import requests
from fastmcp.tools.tool import Tool


def get_issue_relations(
    redmine_url: str,
    api_key: str,
    issue_id: int = None,
    limit: int = None,
    offset: int = None,
):
    """
    Redmine課題のリレーション一覧を取得
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    if issue_id:
        url = f"{redmine_url.rstrip('/')}/issues/{issue_id}/relations.json"
    else:
        url = f"{redmine_url.rstrip('/')}/relations.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    return {
        "relations": data.get("relations", []),
        "total_count": data.get("total_count", 0),
        "limit": data.get("limit", limit if limit is not None else 25),
        "offset": data.get("offset", offset if offset is not None else 0),
    }


GetIssueRelationsTool = Tool.from_function(
    get_issue_relations, name="get_issue_relations", description="Redmine課題のリレーション一覧を取得"
)
