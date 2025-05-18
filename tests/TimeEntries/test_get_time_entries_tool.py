"""Tests for GetTimeEntriesTool."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from tools.TimeEntries.get_time_entries_tool import GetTimeEntriesTool


@pytest.fixture
def tool():
    """Fixture for GetTimeEntriesTool instance."""
    return GetTimeEntriesTool()


def test_get_time_entries_success(tool):
    """Test successful retrieval of time entries."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"time_entries": [], "total_count": 0}
    with patch("requests.get", return_value=mock_response) as mock_get:
        result = tool.run(redmine_url="http://localhost:3000", api_key="dummy", limit=5, project_id="test")
        assert "time_entries" in result
        assert result["total_count"] == 0
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["headers"]["X-Redmine-API-Key"] == "dummy"
        assert kwargs["params"]["limit"] == 5
        assert kwargs["params"]["project_id"] == "test"


def test_get_time_entries_api_error(tool):
    """Test API error handling."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(Exception) as excinfo:
            tool.run(redmine_url="http://localhost:3000", api_key="dummy")
        assert "Failed to get time entries" in str(excinfo.value)
