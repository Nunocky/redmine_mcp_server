import json
import os
import sys
from pprint import pprint

import pytest
from dotenv import load_dotenv

from main import get_issue

load_dotenv()

@pytest.mark.asyncio
async def test_get_issue():
    """Redmine課題取得APIの正常系テスト

    Args:
        なし

    Raises:
        AssertionError: APIレスポンスが期待通りでない場合

    Note:
        REDMINE_URL, REDMINE_API_KEY は .env で設定してください。
        issue_id=1 は存在する課題IDに変更してください。
    """
    issue_id = 1  # 存在する課題IDを指定してください
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_API_KEY")
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert api_key, "REDMINE_API_KEY is not set in .env"

    result = await get_issue(issue_id=issue_id)
    # TextContent型のリストで返る場合に対応
    if isinstance(result, list) and hasattr(result[0], 'text'):
        result_dict = json.loads(result[0].text)
    else:
        result_dict = result
    pprint(result_dict, stream=sys.stderr)
    assert isinstance(result_dict, dict), "APIレスポンスがdict型ではありません"
    assert "issue" in result_dict, "'issue'キーがレスポンスに存在しません"
    assert result_dict["issue"]["id"] == issue_id, "取得した課題IDが一致しません"
