import os

from tools.TimeEntries.create_time_entry_tool import create_time_entry


def test_create_time_entry_real_redmine():
    """
    Integration test to create a new time entry on the actual Redmine server (REDMINE_URL in .env).
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    project_id = os.getenv("REDMINE_TEST_PROJECT_ID", "testproject")
    spent_on = "2025-05-15"
    hours = 1.5
    activity_id = int(os.getenv("REDMINE_TEST_ACTIVITY_ID", "9"))
    comments = "Time entry creation test by pytest"
    result = create_time_entry(
        redmine_url,
        api_key,
        project_id=project_id,
        spent_on=spent_on,
        hours=hours,
        activity_id=activity_id,
        comments=comments,
    )
    assert "time_entry" in result
    assert isinstance(result["time_entry"], dict)
    assert result["time_entry"].get("hours") == hours
    assert result["time_entry"].get("comments") == comments
