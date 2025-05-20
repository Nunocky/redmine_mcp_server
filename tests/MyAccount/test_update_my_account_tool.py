"""Test for get_my_account function in get_my_account_tool.py."""

import os

import pytest

from tools.MyAccount.get_my_account_tool import get_my_account
from tools.MyAccount.update_my_account_tool import update_my_account


@pytest.mark.skip("このテストはスキップされました。")
def test_update_my_account():
    base_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_USER_API_KEY")

    # テスト用の新しい値を生成
    new_firstname = "TestFirst"
    new_lastname = "TestLast"
    import random
    import string

    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    new_mail = f"testuser_{random_str}@example.com"

    result = update_my_account(
        base_url=base_url,
        api_key=api_key,
        firstname=new_firstname,
        lastname=new_lastname,
        mail=new_mail,
    )
    print(result)
    assert isinstance(result, dict)
    assert "user" in result
    user_info = result["user"]
    assert user_info["firstname"] == new_firstname
    assert user_info["lastname"] == new_lastname
    assert user_info["mail"] == new_mail
