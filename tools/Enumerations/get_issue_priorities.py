from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from tools.redmine_api_client import RedmineAPIClient


class GetIssuePrioritiesParams(BaseModel):
    """Params for get_issue_priorities tool."""

    redmine_url: str = Field(description="Redmine server URL")
    api_key: str = Field(description="Redmine API key")
    format: Optional[str] = Field(default="json", description="Response format (xml or json)")


async def get_issue_priorities(
    redmine_url: str,
    api_key: str,
    format: Optional[str] = "json",
) -> Dict[str, Any]:
    """
    Get a list of issue priorities from Redmine.

    Args:
        redmine_url (str): The base URL of the Redmine instance.
        api_key (str): The API key for authentication.
        format (Optional[str]): Response format (xml or json). Defaults to "json".

    Returns:
        Dict[str, Any]: A dictionary containing the list of issue priorities.
    """
    client = RedmineAPIClient(
        base_url=redmine_url,
        api_key=api_key,
    )
    if format not in ["json", "xml"]:
        raise ValueError("format must be 'json' or 'xml'")

    endpoint = f"{redmine_url}/enumerations/issue_priorities.{format}"
    headers = {"X-Redmine-API-Key": api_key, "Content-Type": f"application/{format}"}
    return await client.get(endpoint, headers=headers)
