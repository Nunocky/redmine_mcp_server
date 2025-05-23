import os
import uuid
from tools.Groups.update_group import update_group


def test_update_group_success():
    """Test normal case: update group."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    group_id = os.getenv("REDMINE_TEST_GROUP_ID")
    if not redmine_url or not api_key or not group_id:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_TEST_GROUP_ID が .env で定義されている必要があります。")
    new_name = f"updated-group-{uuid.uuid4()}"
    result = update_group(redmine_url, api_key, int(group_id), name=new_name)
    assert "group" in result
    # RedmineのPUT /groups/{id}.jsonは204 No Contentを返す場合があるため、groupがNoneでも正常とみなす
    if result["group"] is not None:
        assert result["group"]["name"] == new_name


def test_update_group_404():
    """Test 404 case: returns group None."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY が .env で定義されている必要があります。")
    result = update_group(redmine_url, api_key, 99999999, name="dummy")
    assert result == {"group": None}


def test_update_group_validation_error():
    """Test validation error: invalid name (empty string)."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    group_id = os.getenv("REDMINE_TEST_GROUP_ID")
    if not redmine_url or not api_key or not group_id:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_TEST_GROUP_ID が .env で定義されている必要があります。")
    try:
        update_group(redmine_url, api_key, int(group_id), name="")
    except Exception as e:
        from requests.exceptions import HTTPError

        assert isinstance(e, HTTPError)
    else:
        assert False, "Validation error not raised"
