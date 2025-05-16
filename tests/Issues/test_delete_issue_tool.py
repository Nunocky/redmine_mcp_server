import os
from pathlib import Path

from dotenv import load_dotenv

from tools.Issues.create_issue_tool import CreateIssueTool
from tools.Issues.delete_issue_tool import delete_issue


def setup_module(module):
    # .envファイルの絶対パスを指定してロード
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


def test_delete_issue_real_redmine():
    """
    実際のRedmineサーバーの情報を.envから取得し、課題を作成し削除する統合テスト。
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    project_id = "testproject"
    subject = "削除テスト課題 (pytest)"
    description = "pytestによる削除テスト用課題"
    # まず課題を作成
    issue_tool = CreateIssueTool()
    issue = issue_tool.run(project_id, subject, description=description)["issue"]
    issue_id = issue["id"]
    # 削除実行
    result = delete_issue(redmine_url, api_key, issue_id)
    assert result["success"] is True
