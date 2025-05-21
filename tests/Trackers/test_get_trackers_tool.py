"""Integration test for get_trackers (no mock)."""

import os

import pytest

from tools.Trackers.get_trackers import get_trackers

REDMINE_URL = os.environ.get("REDMINE_URL")
REDMINE_API_KEY = os.environ.get("REDMINE_API_KEY")


def test_get_trackers_integration():
    """get_trackers関数でトラッカー一覧が取得できること"""
    api_key = os.getenv("REDMINE_USER_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")

    result = get_trackers(redmine_url, api_key)
    assert isinstance(result, list)
    assert len(result) > 0
    for tracker in result:
        assert "id" in tracker
        assert "name" in tracker
        assert "default_status" in tracker
