from unittest.mock import MagicMock, patch

import pytest

from tools.Projects.unarchive_project_tool import unarchive_project

# test_unarchive_project_tool.py


def test_unarchive_project_success():
    with patch("tools.Projects.unarchive_project_tool.requests.put") as mock_put:
        mock_resp = MagicMock()
        mock_resp.status_code = 204
        mock_resp.text = ""
        mock_put.return_value = mock_resp

        result = unarchive_project("http://example.com", "dummykey", "testproj")
        assert result["status"] == "success"
        assert result["message"] == "Project unarchived"


def test_unarchive_project_error():
    with patch("tools.Projects.unarchive_project_tool.requests.put") as mock_put:
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.text = "Not Found"
        mock_put.return_value = mock_resp

        result = unarchive_project("http://example.com", "dummykey", "testproj")
        assert result["status"] == "error"
        assert result["message"] == "Not Found"
        assert result["status_code"] == 404
