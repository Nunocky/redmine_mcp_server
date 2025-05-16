import os
from pathlib import Path

from dotenv import load_dotenv

from tools.Issues.create_issue_tool import CreateIssueTool
from tools.Issues.delete_issue_tool import delete_issue
from tools.Issues.add_watcher_tool import add_watcher
from tools.Issues.remove_watcher_tool import remove_watcher

def setup_module(module):
    # .envファイルの絶対パスを指定してロード
    load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def test_add_remove_watcher_real_redmine():
    """
    実際のRedmineサーバーで課題にウォッチャーを追加・削除する統合テスト。
    """
    api_key = os.getenv("REDMINE_ADMIN_API_KEY")
    redmine_url = os.getenv("REDMINE_URL")
    watcher_user_id = os.getenv("REDMINE_WATCHER_USER_ID")
    assert api_key, "REDMINE_ADMIN_API_KEY is not set in .env"
    assert redmine_url, "REDMINE_URL is not set in .env"
    assert watcher_user_id, "REDMINE_WATCHER_USER_ID is not set in .env"
    project_id = "testproject"
    subject = "ウォッチャーテスト課題 (pytest)"
    description = "pytestによるウォッチャー追加・削除テスト用課題"
    # 課題作成
    issue_tool = CreateIssueTool()
    issue = issue_tool.run(project_id, subject, description=description)["issue"]
    issue_id = issue["id"]
    # ウォッチャー追加
    add_result = add_watcher(redmine_url, api_key, issue_id, int(watcher_user_id))
    print("add_watcher result:", add_result)
    assert add_result["success"] is True
    # ウォッチャー削除
    remove_result = remove_watcher(redmine_url, api_key, issue_id, int(watcher_user_id))
    print("remove_watcher result:", remove_result)
    assert remove_result["success"] is True
    # 後始末：課題削除
    del_result = delete_issue(redmine_url, api_key, issue_id)
    assert del_result["success"] is True
