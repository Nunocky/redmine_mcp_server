import os
from tools.Groups.get_group import get_group


def test_get_group_success():
    """Test normal case: get group detail."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    group_id = os.getenv("REDMINE_TEST_GROUP_ID")
    if not redmine_url or not api_key or not group_id:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_TEST_GROUP_ID が .env で定義されている必要があります。")
    result = get_group(redmine_url, api_key, int(group_id))
    assert "group" in result
    assert result["group"] is not None


def test_get_group_404():
    """Test 404 case: returns group None."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY が .env で定義されている必要があります。")
    # 存在しないグループIDを指定
    result = get_group(redmine_url, api_key, 99999999)
    assert result == {"group": None}
