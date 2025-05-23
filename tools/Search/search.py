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
    """Redmineリソース横断検索API

    Args:
        redmine_url (str): Redmine base URL
        api_key (str): Redmine API key
        query (str): 検索キーワード
        resource_types (List[str], optional): 検索対象リソース種別（例: ["issues", "projects"]）
        fields (List[str], optional): 検索対象フィールド（例: ["subject", "description"]）
        offset (int, optional): ページネーション開始位置
        limit (int, optional): 取得件数

    Returns:
        Dict[str, Any]: 検索結果・ヒット件数・ページ情報
    """
    if not redmine_url or not api_key or not query:
        raise ValueError("redmine_url, api_key, queryは必須です")

    client = RedmineAPIClient(base_url=redmine_url, api_key=api_key)
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

        for item in items:
            # 検索対象フィールドを決定
            search_fields = fields if fields else meta["fields"]
            text = ""
            for f in search_fields:
                if f in item and item[f]:
                    text += str(item[f]) + " "
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
        total_count += len(results)

    return {
        "results": results[offset : offset + limit],
        "total_count": total_count,
        "offset": offset,
        "limit": limit,
    }
