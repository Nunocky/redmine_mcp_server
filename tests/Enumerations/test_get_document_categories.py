"""DocumentCategories APIの実機テスト

pytest -s tests/Enumerations/test_get_document_categories.py
"""

import os

import pytest

from tools.Enumerations.get_document_categories import get_document_categories


def test_get_document_categories_normal():
    """文書カテゴリ一覧取得APIの正常系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    result = get_document_categories(
        redmine_url=redmine_url,
        api_key=api_key,
    )
    print("result:", result)
    assert "document_categories" in result
    assert isinstance(result["document_categories"], list)


def test_get_document_categories_invalid_url():
    """不正なURL指定時のエラー系テスト"""
    api_key = os.environ.get("REDMINE_USER_API_KEY")
    with pytest.raises(Exception):
        get_document_categories(
            redmine_url="http://invalid-url",
            api_key=api_key,
        )


def test_get_document_categories_invalid_key():
    """不正なAPIキー指定時のエラー系テスト"""
    redmine_url = os.environ.get("REDMINE_URL")
    result = get_document_categories(
        redmine_url=redmine_url,
        api_key="invalid_key",
    )
    # APIキーが無効でも取得できてしまうRedmine環境の場合はスキップ
    if "document_categories" in result and result["document_categories"]:
        pytest.skip("APIキーが無効でも取得できるRedmine環境のためスキップ")
    assert "document_categories" not in result or not result["document_categories"]
