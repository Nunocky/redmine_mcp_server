"""Integration tests for get_trackers function (no mock)."""

import os

import pytest

from tools.Trackers.get_trackers import get_trackers

REDMINE_URL = os.environ.get("REDMINE_URL")
REDMINE_API_KEY = os.environ.get("REDMINE_API_KEY")


def test_get_trackers_integration():
    """実APIでトラッカー一覧が取得できること"""
    api_key = os.getenv("REDMINE_USER_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")

    trackers = get_trackers(redmine_url, api_key)
    assert isinstance(trackers, list)
    assert len(trackers) > 0
    for tracker in trackers:
        assert "id" in tracker
        assert "name" in tracker
        assert "default_status" in tracker
        # descriptionはnull許容
        assert "description" in tracker
        # enabled_standard_fieldsはRedmine 5.0+のみ
        if "enabled_standard_fields" in tracker:
            assert isinstance(tracker["enabled_standard_fields"], list)
