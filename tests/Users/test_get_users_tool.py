import os
from pprint import pprint
import sys
import pytest

from tools.Users.get_users_tool import GetUsersTool

@pytest.fixture
def tool():
    return GetUsersTool()

def test_run_success(tool):
    """
    実際のRedmineサーバーにアクセスしてユーザー一覧を取得し、基本的な項目を検証する。
    """
    # 環境変数の設定
    os.environ["REDMINE_API_KEY"] = os.getenv("REDMINE_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_API_KEY"], "REDMINE_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # 実行
    result = tool.run(limit=5)
    pprint(result, stream=sys.stderr)

    # 検証
    assert "users" in result
    assert isinstance(result["users"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result
    assert result["limit"] == 5

def test_run_with_status_filter(tool):
    """
    status フィルタを使用してユーザー一覧を取得し、結果を検証する。
    """
    # 環境変数の設定
    os.environ["REDMINE_API_KEY"] = os.getenv("REDMINE_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_API_KEY"], "REDMINE_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # 実行 (アクティブユーザーのみ)
    result = tool.run(status=1, limit=5)
    pprint(result, stream=sys.stderr)

    # 検証
    assert "users" in result
    assert isinstance(result["users"], list)

    # すべてのユーザーがアクティブであることを確認
    # 注: APIレスポンスにstatusが含まれない場合はスキップ
    for user in result["users"]:
        if "status" in user:
            assert user["status"] == 1

def test_run_with_name_filter(tool):
    """
    name フィルタを使用してユーザー一覧を取得し、結果を検証する。
    """
    # 環境変数の設定
    os.environ["REDMINE_API_KEY"] = os.getenv("REDMINE_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_API_KEY"], "REDMINE_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # テスト用のユーザー名（環境に合わせて変更）
    test_name = os.getenv("REDMINE_TEST_USER_NAME", "admin")

    # 実行
    result = tool.run(name=test_name)
    pprint(result, stream=sys.stderr)

    # 検証
    assert "users" in result
    assert isinstance(result["users"], list)

    # 少なくとも1人のユーザーが見つかることを確認
    assert len(result["users"]) > 0

    # 検索結果にtest_nameが含まれていることを確認
    found = False
    for user in result["users"]:
        if (
            test_name.lower() in user.get("login", "").lower() or
            test_name.lower() in user.get("firstname", "").lower() or
            test_name.lower() in user.get("lastname", "").lower() or
            test_name.lower() in user.get("mail", "").lower()
        ):
            found = True
            break

    assert found, f"検索結果に '{test_name}' が含まれていません"

def test_run_with_group_id_filter(tool):
    """
    group_id フィルタを使用してユーザー一覧を取得し、結果を検証する。
    注: このテストはグループが存在する環境でのみ成功します。
    """
    # 環境変数の設定
    os.environ["REDMINE_API_KEY"] = os.getenv("REDMINE_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_API_KEY"], "REDMINE_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # テスト用のグループID（環境に合わせて変更）
    test_group_id = os.getenv("REDMINE_TEST_GROUP_ID")

    # グループIDが設定されていない場合はスキップ
    if not test_group_id:
        pytest.skip("REDMINE_TEST_GROUP_ID is not set in .env")

    # 実行
    result = tool.run(group_id=int(test_group_id))
    pprint(result, stream=sys.stderr)

    # 検証
    assert "users" in result
    assert isinstance(result["users"], list)

def test_run_with_pagination(tool):
    """
    limit と offset を使用したページネーションのテスト
    """
    # 環境変数の設定
    os.environ["REDMINE_API_KEY"] = os.getenv("REDMINE_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_API_KEY"], "REDMINE_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # 1ページ目を取得 (最初の2件)
    result_page1 = tool.run(limit=2, offset=0)
    pprint(result_page1, stream=sys.stderr)

    # 2ページ目を取得 (次の2件)
    result_page2 = tool.run(limit=2, offset=2)
    pprint(result_page2, stream=sys.stderr)

    # 検証
    assert "users" in result_page1
    assert "users" in result_page2
    assert isinstance(result_page1["users"], list)
    assert isinstance(result_page2["users"], list)
    assert result_page1["limit"] == 2
    assert result_page2["limit"] == 2
    assert result_page1["offset"] == 0
    assert result_page2["offset"] == 2

    # 十分なユーザーがいる場合、異なるユーザーが取得されることを確認
    if len(result_page1["users"]) > 0 and len(result_page2["users"]) > 0:
        if "id" in result_page1["users"][0] and "id" in result_page2["users"][0]:
            assert result_page1["users"][0]["id"] != result_page2["users"][0]["id"]

def test_run_with_combined_filters(tool):
    """
    複数のフィルタを組み合わせたテスト
    """
    # 環境変数の設定
    os.environ["REDMINE_API_KEY"] = os.getenv("REDMINE_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_API_KEY"], "REDMINE_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # テスト用のユーザー名（環境に合わせて変更）
    test_name = os.getenv("REDMINE_TEST_USER_NAME", "admin")

    # 実行 (アクティブユーザーかつ特定の名前を持つユーザー)
    result = tool.run(status=1, name=test_name, limit=5)
    pprint(result, stream=sys.stderr)

    # 検証
    assert "users" in result
    assert isinstance(result["users"], list)

    # 結果が存在する場合、条件を満たすことを確認
    if len(result["users"]) > 0:
        for user in result["users"]:
            # statusが含まれている場合は確認
            if "status" in user:
                assert user["status"] == 1

            # 名前が含まれていることを確認
            found = False
            if (
                test_name.lower() in user.get("login", "").lower() or
                test_name.lower() in user.get("firstname", "").lower() or
                test_name.lower() in user.get("lastname", "").lower() or
                test_name.lower() in user.get("mail", "").lower()
            ):
                found = True

            assert found, f"ユーザー {user.get('login')} は検索条件 '{test_name}' を満たしていません"
