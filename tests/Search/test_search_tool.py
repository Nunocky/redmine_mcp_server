import os

from tools.Search.search import search


def test_search_issues():
    """issuesリソースのキーワード検索テスト"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_USER_API_KEY"]
    result = search(
        redmine_url=redmine_url,
        api_key=api_key,
        query="test",
        resource_types=["issues"],
        fields=["subject", "description"],
        offset=0,
        limit=5,
    )
    assert "results" in result
    assert isinstance(result["results"], list)
    assert result["offset"] == 0
    assert result["limit"] == 5


def test_search_projects():
    """projectsリソースのキーワード検索テスト"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_USER_API_KEY"]
    result = search(
        redmine_url=redmine_url,
        api_key=api_key,
        query="Redmine",
        resource_types=["projects"],
        fields=["name", "description"],
        offset=0,
        limit=3,
    )
    assert "results" in result
    assert isinstance(result["results"], list)
    assert result["offset"] == 0
    assert result["limit"] == 3


def test_search_invalid_resource():
    """存在しないリソース指定時の動作テスト"""
    redmine_url = os.environ["REDMINE_URL"]
    api_key = os.environ["REDMINE_USER_API_KEY"]
    result = search(
        redmine_url=redmine_url,
        api_key=api_key,
        query="dummy",
        resource_types=["notfound"],
        offset=0,
        limit=2,
    )
    assert "results" in result
    assert result["results"] == []
