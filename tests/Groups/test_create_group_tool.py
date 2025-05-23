import os
import uuid
from tools.Groups.create_group import create_group


def test_create_group_success():
    """Test normal case: create group."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY が .env で定義されている必要があります。")
    group_name = f"test-group-{uuid.uuid4()}"
    result = create_group(redmine_url, api_key, name=group_name)
    assert "group" in result
    assert result["group"]["name"] == group_name


def test_create_group_validation_error():
    """Test validation error: missing name."""
    redmine_url = os.getenv("REDMINE_URL")
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    if not redmine_url or not api_key:
        raise RuntimeError("REDMINE_URL, REDMINE_ADMIN_API_KEY が .env で定義されている必要があります。")
    try:
        create_group(redmine_url, api_key, name=None)
    except Exception as e:
        # Redmineは422エラー時に詳細なバリデーションメッセージを返さない場合があるため、HTTPError例外であればOKとする
        from requests.exceptions import HTTPError

        assert isinstance(e, HTTPError)
    else:
        assert False, "Validation error not raised"
