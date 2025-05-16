"""Redmine Issue Details Retrieval Tool"""

import requests
from fastmcp.tools.tool import Tool


def get_issue(
    redmine_url: str,
    api_key: str,
    issue_id: int,
    include: str = None,
):
    """
    Get detailed information for the specified issue (issue_id)

    Args:
        redmine_url (str): Base URL of Redmine
        api_key (str): API key
        issue_id (int): Issue ID
        include (str, optional): Additional information (comma-separated)

    Returns:
        dict: Issue details information
    """
    import os

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    headers = {"X-Redmine-API-Key": api_key}
    params = {}
    if include:
        params["include"] = include
    url = f"{redmine_url.rstrip('/')}/issues/{issue_id}.json"
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()


GetIssueTool = Tool.from_function(get_issue, name="get_issue", description="Get Redmine issue information")
