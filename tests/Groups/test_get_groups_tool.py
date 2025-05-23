import os
from tools.Groups.get_groups import get_groups


def test_get_groups_success():
    """Test normal case: get groups list."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY が .env で定義されている必要があります。")
    result = get_groups(redmine_url, api_key)
    assert "groups" in result
    assert isinstance(result["groups"], list)
