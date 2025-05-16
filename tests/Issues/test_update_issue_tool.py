import os
from pathlib import Path

from dotenv import load_dotenv

from tools.Issues.create_issue_tool import CreateIssueTool
from tools.Issues.update_issue_tool import update_issue
from tools.Issues.delete_issue_tool import delete_issue

def setup_module(module):
    # .envファイルの絶対パスを指定してロード
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def test_update_issue_real_redmine():
    """
    実際のRedmineサーバーの情報を.envから取得し、課題を作成し更新する統合テスト。
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    project_id = "testproject"
    subject = "更新テスト課題 (pytest)"
    description = "pytestによる更新テスト用課題"
    # まず課題を作成
    issue_tool = CreateIssueTool()
    issue = issue_tool.run(project_id, subject, description=description)["issue"]
    issue_id = issue["id"]
    # 更新内容
    new_subject = "更新後の課題タイトル (pytest)"
    new_description = "課題説明を更新しました"
    result = update_issue(redmine_url, api_key, issue_id, subject=new_subject, description=new_description)
    print("update_issue result:", result)
    assert result["success"] is True
    # テストで作成した課題を削除
    del_result = delete_issue(redmine_url, api_key, issue_id)
    assert del_result["success"] is True
