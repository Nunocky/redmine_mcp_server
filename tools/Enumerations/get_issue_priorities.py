from typing import Any, Dict

from tools.redmine_api_client import RedmineAPIClient


def get_issue_priorities(
    redmine_url: str,
    api_key: str,
) -> Dict[str, Any]:
    """Get a list of issue priorities from Redmine.

    Args:
        redmine_url (str): The base URL of the Redmine instance.
        api_key (str): The API key for authentication.

    Returns:
        dict: A dictionary containing the list of issue priorities.

    Raises:
        ValueError: If required parameters are missing.
        Exception: When API request fails (excluding 404 errors)
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )

    endpoint = "/enumerations/issue_priorities.json"

    try:
        response = client.get(
            endpoint=endpoint,
            params={},
        )
        data = response.json()
        return data
    except Exception as e:
        if hasattr(e, "response") and e.response is not None and getattr(e.response, "status_code", None) == 404:
            raise ValueError("指定されたリソースは存在しません") from e
        raise
