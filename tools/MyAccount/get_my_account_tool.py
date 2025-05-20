from typing import Any, Dict, Optional

from tools.redmine_api_client import RedmineAPIClient


def get_my_account(
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Get the current user's account information using RedmineAPIClient.

    Args:
        base_url (str, optional): Redmine server base URL
        api_key (str, optional): Redmine API key

    Returns:
        dict: User account information

    Raises:
        Exception: If the API request fails or response is invalid
    """
    client = RedmineAPIClient(base_url=base_url, api_key=api_key)
    endpoint = "/my/account.json"
    try:
        response = client.get(endpoint)
        data = response.json()
        return data
    except Exception as e:
        raise Exception(f"Failed to get account info: {e}")
