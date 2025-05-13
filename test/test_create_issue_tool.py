import os
from pathlib import Path

from dotenv import load_dotenv

from tools.create_issue_tool import create_issue

# .envファイルの絶対パスを指定してロード
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


def test_create_issue_real_redmine():
    """
    実際のRedmineサーバー(.envのREDMINE_URL)に新しいissueを作成する統合テスト。
    """
    api_key = os.getenv("REDMINE_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    project_id = "testproject"
    subject = "テスト課題 (pytest)"
    description = "pytestによる自動作成テスト"
    result = create_issue(redmine_url, api_key, project_id, subject, description=description)
    assert "issue" in result
    assert isinstance(result["issue"], dict)
    assert result["issue"].get("subject") == subject
