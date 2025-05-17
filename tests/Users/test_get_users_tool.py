import os
import sys
from pprint import pprint

import pytest

from tools.Users.get_users_tool import GetUsersTool
from unwrap_text_content import unwrap_text_content


@pytest.mark.asyncio
async def test_run_success():
    """
    Access the actual Redmine server to retrieve the user list and verify basic items.
    """
    # Set environment variables
    os.environ["REDMINE_ADMIN_API_KEY"] = os.getenv("REDMINE_ADMIN_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_ADMIN_API_KEY"], "REDMINE_ADMIN_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # Execute
    tool = GetUsersTool
    result = await tool.run({"limit": 5})
    result = unwrap_text_content(result)
    pprint(result, stream=sys.stderr)

    # Verify
    assert "users" in result
    assert isinstance(result["users"], list)
    assert "total_count" in result
    assert "limit" in result
    assert "offset" in result
    assert result["limit"] == 5


@pytest.mark.asyncio
async def test_run_with_status_filter():
    """
    Use the status filter to retrieve the user list and verify the results.
    """
    # Set environment variables
    os.environ["REDMINE_ADMIN_API_KEY"] = os.getenv("REDMINE_ADMIN_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_ADMIN_API_KEY"], "REDMINE_ADMIN_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # Execute (active users only)
    tool = GetUsersTool
    result = await tool.run({"status": 1, "limit": 5})
    result = unwrap_text_content(result)
    pprint(result, stream=sys.stderr)

    # Verify
    assert "users" in result
    assert isinstance(result["users"], list)

    # Confirm that all users are active
    # Note: Skip if status is not included in the API response
    for user in result["users"]:
        if "status" in user:
            assert user["status"] == 1


@pytest.mark.asyncio
async def test_run_with_name_filter():
    """
    Use the name filter to retrieve the user list and verify the results.
    """
    # Set environment variables
    os.environ["REDMINE_ADMIN_API_KEY"] = os.getenv("REDMINE_ADMIN_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_ADMIN_API_KEY"], "REDMINE_ADMIN_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # Test username (change according to your environment)
    test_name = os.getenv("REDMINE_TEST_USER_NAME", "admin")

    # Execute
    tool = GetUsersTool
    result = await tool.run({"name": test_name})
    result = unwrap_text_content(result)
    pprint(result, stream=sys.stderr)

    # Verify
    assert "users" in result
    assert isinstance(result["users"], list)

    # Confirm that at least one user is found
    assert len(result["users"]) > 0

    # Confirm that test_name is included in the search results
    found = False
    for user in result["users"]:
        if (
            test_name.lower() in user.get("login", "").lower()
            or test_name.lower() in user.get("firstname", "").lower()
            or test_name.lower() in user.get("lastname", "").lower()
            or test_name.lower() in user.get("mail", "").lower()
        ):
            found = True
            break

    assert found, f"Search results do not include '{test_name}'"


@pytest.mark.asyncio
async def test_run_with_group_id_filter():
    """
    Use the group_id filter to retrieve the user list and verify the results.
    Note: This test will only succeed in an environment where groups exist.
    """
    # Set environment variables
    os.environ["REDMINE_ADMIN_API_KEY"] = os.getenv("REDMINE_ADMIN_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_ADMIN_API_KEY"], "REDMINE_ADMIN_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # Test group ID
    test_group_id = 3  # non member group ID

    # Execute
    result = await GetUsersTool.run({"group_id": int(test_group_id)})
    result = unwrap_text_content(result)
    pprint(result, stream=sys.stderr)

    # Verify
    assert "users" in result
    assert isinstance(result["users"], list)


@pytest.mark.asyncio
async def test_run_with_pagination():
    """
    Test pagination using limit and offset
    """
    # Set environment variables
    os.environ["REDMINE_ADMIN_API_KEY"] = os.getenv("REDMINE_ADMIN_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_ADMIN_API_KEY"], "REDMINE_ADMIN_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # Get the first page (first 2 items)
    result_page1 = await GetUsersTool.run({"limit": 2, "offset": 0})
    result_page1 = unwrap_text_content(result_page1)
    pprint(result_page1, stream=sys.stderr)

    # Get the second page (next 2 items)
    result_page2 = await GetUsersTool.run({"limit": 2, "offset": 2})
    result_page2 = unwrap_text_content(result_page2)
    pprint(result_page2, stream=sys.stderr)

    # Verify
    assert "users" in result_page1
    assert "users" in result_page2
    assert isinstance(result_page1["users"], list)
    assert isinstance(result_page2["users"], list)
    assert result_page1["limit"] == 2
    assert result_page2["limit"] == 2
    assert result_page1["offset"] == 0
    assert result_page2["offset"] == 2

    # If there are enough users, confirm that different users are retrieved
    if len(result_page1["users"]) > 0 and len(result_page2["users"]) > 0:
        if "id" in result_page1["users"][0] and "id" in result_page2["users"][0]:
            assert result_page1["users"][0]["id"] != result_page2["users"][0]["id"]


@pytest.mark.asyncio
async def test_run_with_combined_filters():
    """
    Test combining multiple filters
    """
    # Set environment variables
    os.environ["REDMINE_ADMIN_API_KEY"] = os.getenv("REDMINE_ADMIN_API_KEY", "")
    os.environ["REDMINE_URL"] = os.getenv("REDMINE_URL", "")

    assert os.environ["REDMINE_ADMIN_API_KEY"], "REDMINE_ADMIN_API_KEY is not set in .env"
    assert os.environ["REDMINE_URL"], "REDMINE_URL is not set in .env"

    # Test username (change according to your environment)
    test_name = os.getenv("REDMINE_TEST_USER_NAME", "admin")

    # Execute (active users with a specific name)
    result = await GetUsersTool.run({"status": 1, "name": test_name, "limit": 5})
    result = unwrap_text_content(result)
    pprint(result, stream=sys.stderr)

    # Verify
    assert "users" in result
    assert isinstance(result["users"], list)

    # If results exist, confirm that they meet the conditions
    if len(result["users"]) > 0:
        for user in result["users"]:
            # Confirm if status is included
            if "status" in user:
                assert user["status"] == 1

            # Confirm that the name is included
            found = False
            if (
                test_name.lower() in user.get("login", "").lower()
                or test_name.lower() in user.get("firstname", "").lower()
                or test_name.lower() in user.get("lastname", "").lower()
                or test_name.lower() in user.get("mail", "").lower()
            ):
                found = True

            assert found, f"User {user.get('login')} does not meet the search criteria '{test_name}'"
