import os
from tools.Groups.delete_group import delete_group
from tools.Groups.create_group import create_group


def test_delete_group_success():
    """Test normal case: delete group."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY が .env で定義されている必要があります。")
    # まずグループを作成
    group_name = "delete-test-group"
    group = create_group(redmine_url, api_key, name=group_name)
    group_id = group["group"]["id"]
    # 削除
    result = delete_group(redmine_url, api_key, group_id)
    assert result == {"success": True}


def test_delete_group_404():
    """Test 404 case: returns not found."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY が .env で定義されている必要があります。")
    result = delete_group(redmine_url, api_key, 99999999)
    assert result == {"success": False, "error": "Not found"}
