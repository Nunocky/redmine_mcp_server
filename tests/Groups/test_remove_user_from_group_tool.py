import os
from tools.Groups.create_group import create_group
from tools.Groups.delete_group import delete_group
from tools.Groups.add_user_to_group import add_user_to_group
from tools.Groups.remove_user_from_group import remove_user_from_group


def test_remove_user_from_group_success():
    """Test normal case: remove user from group."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    user_id = os.getenv("REDMINE_USER_ID")
    if not redmine_url or not api_key or not user_id:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_USER_ID が .env で定義されている必要があります。")
    # グループを作成
    group = create_group(redmine_url, api_key, name="remove-user-test-group")
    group_id = group["group"]["id"]
    # ユーザー追加
    add_user_to_group(redmine_url, api_key, group_id, [int(user_id)])
    # ユーザー削除
    result = remove_user_from_group(redmine_url, api_key, group_id, int(user_id))
    assert result == {"success": True}
    # 後始末
    delete_group(redmine_url, api_key, group_id)


def test_remove_user_from_group_404():
    """Test 404 case: returns not found."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    user_id = os.getenv("REDMINE_USER_ID")
    if not redmine_url or not api_key or not user_id:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_USER_ID が .env で定義されている必要があります。")
    result = remove_user_from_group(redmine_url, api_key, 99999999, int(user_id))
    assert result == {"success": False, "error": "Not found"}
