"""Redmineリソース横断検索API

RedmineのIssues, Projects, News, WikiPages等を対象に
キーワードや条件で横断的に検索を行うAPI関数
"""

from typing import Any, Dict, List, Optional

import requests

from tools.redmine_api_client import RedmineAPIClient


def search(
    redmine_url: str,
    api_key: str,
    query: str,
    resource_types: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    offset: int = 0,
    limit: int = 20,
) -> Dict[str, Any]:
    """Cross-resource Redmine search API

    Args:
        redmine_url (str): Redmine base URL
        api_key (str): Redmine API key
        query (str): Search keyword
        resource_types (List[str], optional): Target resource types to search (e.g., ["issues", "projects"])
        fields (List[str], optional): Fields to search (e.g., ["subject", "description"])
        offset (int, optional): Pagination start position
        limit (int, optional): Number of items to retrieve

    Returns:
        Dict[str, Any]: Search results, hit count, and pagination info
    """
    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key,)
    results = []
    total_count = 0

    # デフォルトリソース
    all_resources = {
        "issues": {
            "endpoint": "/issues.json",
            "fields": ["subject", "description", "notes"],
            "id_field": "id",
            "title_field": "subject",
            "desc_field": "description",
            "url_fmt": "{base}/issues/{id}",
            "list_key": "issues",
        },
        "projects": {
            "endpoint": "/projects.json",
            "fields": ["name", "description"],
            "id_field": "id",
            "title_field": "name",
            "desc_field": "description",
            "url_fmt": "{base}/projects/{id}",
            "list_key": "projects",
        },
        "news": {
            "endpoint": "/news.json",
            "fields": ["title", "description", "summary"],
            "id_field": "id",
            "title_field": "title",
            "desc_field": "description",
            "url_fmt": "{base}/news/{id}",
            "list_key": "news",
        },
        "wikipages": {
            "endpoint": "/wiki/index.json",
            "fields": ["title"],
            "id_field": "id",
            "title_field": "title",
            "desc_field": None,
            "url_fmt": "{base}/wiki/{title}",
            "list_key": "wiki_pages",
        },
    }

    if resource_types is None:
        resource_types = ["issues", "projects", "news", "wikipages"]

    for resource in resource_types:
        if resource not in all_resources:
            continue
        meta = all_resources[resource]
        params = {"offset": offset, "limit": limit}
        try:
            response = client.get(endpoint=meta["endpoint"], params=params)
            items = response.json().get(meta["list_key"], [])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                continue
            raise

        resource_matches = 0  # 追加: 各リソースごとのマッチ数
        for item in items:
            # 検索対象フィールドを決定
            search_fields = fields if fields else meta["fields"]
            text_parts = []
            for f in search_fields:
                if f in item and item[f]:
                    text_parts.append(str(item[f]))
            text = " ".join(text_parts)
            if query.lower() in text.lower():
                result = {
                    "resource_type": resource,
                    "id": item.get(meta["id_field"]),
                    "title": item.get(meta["title_field"]),
                    "description": item.get(meta["desc_field"]) if meta["desc_field"] else "",
                    "url": meta["url_fmt"].format(
                        base=redmine_url.rstrip("/"),
                        id=item.get(meta["id_field"]),
                        title=item.get(meta["title_field"]),
                    ),
                }
                results.append(result)
                resource_matches += 1  # 追加: マッチ数カウント
        total_count += resource_matches  # 修正: 新規マッチ数のみ加算

    return {
        "results": results[offset : offset + limit],
        "total_count": total_count,
        "offset": offset,
        "limit": limit,
    }
