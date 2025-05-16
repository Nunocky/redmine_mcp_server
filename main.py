"""MCPサーバエントリポイント

Redmine MCPサーバとしてtools配下の全APIツールを@mcp.tool()で登録し、サーバを起動する。
"""

import asyncio
import json
import os

from fastmcp.server import FastMCP

from tools.get_memberships_tool import GetMembershipsTool
from tools.get_news_tool import GetNewsTool
from tools.get_queries_tool import GetQueriesTool
from tools.get_versions_tool import GetVersionTool
from tools.get_wiki_pages_tool import GetWikiPagesTool
from tools.Issues.add_watcher_tool import AddWatcherTool
from tools.Issues.create_issue_tool import CreateIssueTool
from tools.Issues.delete_issue_tool import DeleteIssueTool
from tools.Issues.get_issue_relations_tool import GetIssueRelationsTool
from tools.Issues.get_issue_tool import GetIssueTool
from tools.Issues.get_issues_tool import GetIssuesTool
from tools.Issues.remove_watcher_tool import RemoveWatcherTool
from tools.Issues.update_issue_tool import UpdateIssueTool
from tools.Projects.archive_project_tool import ArchiveProjectTool
from tools.Projects.create_project_tool import CreateProjectTool
from tools.Projects.delete_project_tool import DeleteProjectTool
from tools.Projects.get_project_tool import GetProjectTool
from tools.Projects.get_projects_tool import GetProjectsTool
from tools.Projects.unarchive_project_tool import UnarchiveProjectTool
from tools.Projects.update_project_tool import UpdateProjectTool
from tools.TimeEntries.create_time_entry_tool import CreateTimeEntryTool
from tools.TimeEntries.get_time_entries_tool import GetTimeEntriesTool
from tools.Users.create_user_tool import CreateUserTool
from tools.Users.delete_user_tool import DeleteUserTool
from tools.Users.get_user_tool import GetUserTool
from tools.Users.get_users_tool import GetUsersTool
from tools.Users.update_user_tool import UpdateUserTool

mcp = FastMCP("Redmine MCP Server", "0.1.0")


@mcp.tool()
async def get_memberships(
    redmine_url: str,
    api_key: str,
    project_id: str,
) -> dict:
    """指定したプロジェクトのメンバーシップ一覧を取得"""
    result = await GetMembershipsTool.run(
        {
            "redmine_url": redmine_url,
            "api_key": api_key,
            "project_id": project_id,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def get_news(
    redmine_url: str = None,
    api_key: str = None,
    project_id: str = None,
    limit: int = None,
    offset: int = None,
) -> dict:
    """Redmineニュース一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await GetNewsTool.run(
        {
            "redmine_url": redmine_url,
            "api_key": api_key,
            "project_id": project_id,
            "limit": limit,
            "offset": offset,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def get_queries_tool(
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineクエリ一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")

    result = await GetQueriesTool.run(
        {
            "redmine_url": redmine_url,
            "api_key": api_key,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def get_versions(
    redmine_url: str = None,
    api_key: str = None,
    project_id: str = None,
    limit: int = None,
    offset: int = None,
) -> dict:
    """Redmineバージョン一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await GetVersionTool.run(
        redmine_url,
        api_key,
        project_id,
        limit,
        offset,
    )


@mcp.tool()
async def get_wiki_pages(
    redmine_url: str = None,
    api_key: str = None,
    project_id: str = None,
) -> dict:
    """Redmine Wikiページ一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await GetWikiPagesTool.run(
        redmine_url,
        api_key,
        project_id,
    )


@mcp.tool()
async def create_issue(
    project_id: str,
    subject: str,
    description: str = None,
    tracker_id: int = None,
    status_id: int = None,
    priority_id: int = None,
    category_id: int = None,
    fixed_version_id: int = None,
    assigned_to_id: int = None,
    parent_issue_id: int = None,
    custom_fields=None,
    watcher_user_ids=None,
    is_private: bool = None,
    estimated_hours: float = None,
    uploads=None,
) -> dict:
    """Redmine課題を作成"""
    return CreateIssueTool().run(
        project_id,
        subject,
        description,
        tracker_id,
        status_id,
        priority_id,
        category_id,
        fixed_version_id,
        assigned_to_id,
        parent_issue_id,
        custom_fields,
        watcher_user_ids,
        is_private,
        estimated_hours,
        uploads,
    )


@mcp.tool()
async def get_issue(
    issue_id: int,
    include: str = None,
) -> dict:
    """Redmine課題詳細を取得"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")

    return await GetIssueTool.run(
        {
            "redmine_url": redmine_url,
            "api_key": api_key,
            "issue_id": issue_id,
            "include": include if include is not None else "",
        }
    )


@mcp.tool()
async def get_issues(
    offset: int = None,
    limit: int = None,
    sort: str = None,
    include: str = None,
    filters: dict = None,
) -> dict:
    """Redmine課題一覧を取得"""
    # runは同期関数なので、async対応のためスレッド実行
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: GetIssuesTool().run(offset, limit, sort, include, filters))


@mcp.tool()
async def add_watcher(
    issue_id: int,
    user_id: int,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmine課題にウォッチャーを追加"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")

    return AddWatcherTool.run(
        {
            "redmine_url": redmine_url,
            "api_key": api_key,
            "issue_id": issue_id,
            "user_id": user_id,
        }
    )


@mcp.tool()
async def remove_watcher(
    issue_id: int,
    user_id: int,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmine課題からウォッチャーを削除"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await RemoveWatcherTool.run(
        redmine_url,
        api_key,
        issue_id,
        user_id,
    )


@mcp.tool()
async def delete_issue(
    issue_id: int,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmine課題を削除"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await DeleteIssueTool.run(
        redmine_url,
        api_key,
        issue_id,
    )


@mcp.tool()
async def get_issue_relations(
    issue_id: int = None,
    limit: int = None,
    offset: int = None,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmine課題のリレーション一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")

    return await GetIssueRelationsTool.run(
        {
            "redmine_url": redmine_url,
            "api_key": api_key,
            "issue_id": issue_id,
            "limit": limit,
            "offset": offset,
        }
    )


@mcp.tool()
async def update_issue(
    issue_id: int,
    subject: str = None,
    description: str = None,
    tracker_id: int = None,
    status_id: int = None,
    priority_id: int = None,
    category_id: int = None,
    fixed_version_id: int = None,
    assigned_to_id: int = None,
    parent_issue_id: int = None,
    custom_fields=None,
    watcher_user_ids=None,
    is_private: bool = None,
    estimated_hours: float = None,
    notes: str = None,
    private_notes: bool = None,
    uploads=None,
) -> dict:
    """Redmine課題を更新"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await UpdateIssueTool.run(
        redmine_url,
        api_key,
        issue_id,
        subject,
        description,
        tracker_id,
        status_id,
        priority_id,
        category_id,
        fixed_version_id,
        assigned_to_id,
        parent_issue_id,
        custom_fields,
        watcher_user_ids,
        is_private,
        estimated_hours,
        notes,
        private_notes,
        uploads,
    )


@mcp.tool()
async def archive_project(
    project_id_or_identifier: str,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineプロジェクトをアーカイブ"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await ArchiveProjectTool.run(
        {
            "project_id_or_identifier": project_id_or_identifier,
            "redmine_url": redmine_url,
            "api_key": api_key,
        }
    )
    # TextContentでラップされている場合はアンラップ
    return unwrap_text_content(result)


@mcp.tool()
async def create_project(
    name: str,
    identifier: str,
    redmine_url: str = None,
    api_key: str = None,
    description: str = None,
    homepage: str = None,
    is_public: bool = None,
    parent_id: int = None,
    inherit_members: bool = None,
    default_assigned_to_id: int = None,
    default_version_id: int = None,
    tracker_ids=None,
    enabled_module_names=None,
    issue_custom_field_ids=None,
    custom_field_values=None,
) -> dict:
    """Redmineプロジェクトを作成"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await CreateProjectTool.run(
        {
            "name": name,
            "identifier": identifier,
            "redmine_url": redmine_url,
            "api_key": api_key,
            "description": description,
            "homepage": homepage,
            "is_public": is_public,
            "parent_id": parent_id,
            "inherit_members": inherit_members,
            "default_assigned_to_id": default_assigned_to_id,
            "default_version_id": default_version_id,
            "tracker_ids": tracker_ids,
            "enabled_module_names": enabled_module_names,
            "issue_custom_field_ids": issue_custom_field_ids,
            "custom_field_values": custom_field_values,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def delete_project(
    project_id_or_identifier: str,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineプロジェクトを削除"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await DeleteProjectTool.run(
        {
            "project_id_or_identifier": project_id_or_identifier,
            "redmine_url": redmine_url,
            "api_key": api_key,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def unarchive_project(
    project_id_or_identifier: str,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineプロジェクトのアーカイブ解除"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await UnarchiveProjectTool.run(
        {
            "project_id_or_identifier": project_id_or_identifier,
            "redmine_url": redmine_url,
            "api_key": api_key,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def update_project(
    project_id_or_identifier: str,
    redmine_url: str = None,
    api_key: str = None,
    name: str = None,
    description: str = None,
    homepage: str = None,
    is_public: bool = None,
    parent_id: int = None,
    inherit_members: bool = None,
    default_assigned_to_id: int = None,
    default_version_id: int = None,
    tracker_ids=None,
    enabled_module_names=None,
    issue_custom_field_ids=None,
    custom_field_values=None,
) -> dict:
    """Redmineプロジェクトを更新"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await UpdateProjectTool.run(
        {
            "project_id_or_identifier": project_id_or_identifier,
            "redmine_url": redmine_url,
            "api_key": api_key,
            "name": name,
            "description": description,
            "homepage": homepage,
            "is_public": is_public,
            "parent_id": parent_id,
            "inherit_members": inherit_members,
            "default_assigned_to_id": default_assigned_to_id,
            "default_version_id": default_version_id,
            "tracker_ids": tracker_ids,
            "enabled_module_names": enabled_module_names,
            "issue_custom_field_ids": issue_custom_field_ids,
            "custom_field_values": custom_field_values,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def get_project(
    project_id_or_identifier: str,
    include: str = None,
) -> dict:
    """Redmineプロジェクト詳細を取得"""
    redmine_url = os.environ.get("REDMINE_URL")
    api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await GetProjectTool.run(
        {
            "project_id_or_identifier": project_id_or_identifier,
            "redmine_url": redmine_url,
            "api_key": api_key,
            "include": include,
        }
    )
    # TextContentでラップされている場合はアンラップ
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def get_projects_tool(
    redmine_url: str = None,
    api_key: str = None,
    include: str = None,
    limit: int = None,
    offset: int = None,
) -> dict:
    """Redmineプロジェクト一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    result = await GetProjectsTool.run(
        {
            "redmine_url": redmine_url,
            "api_key": api_key,
            "include": include,
            "limit": limit,
            "offset": offset,
        }
    )
    if isinstance(result, list) and len(result) == 1 and hasattr(result[0], "text"):
        return json.loads(result[0].text)
    return result


@mcp.tool()
async def create_time_entry(
    issue_id: int = None,
    project_id: str = None,
    spent_on: str = None,
    hours: float = None,
    activity_id: int = None,
    comments: str = None,
    user_id: int = None,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineで新しいタイムエントリを作成"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await CreateTimeEntryTool.run(
        redmine_url,
        api_key,
        issue_id,
        project_id,
        spent_on,
        hours,
        activity_id,
        comments,
        user_id,
    )


@mcp.tool()
async def get_time_entries(
    project_id: str = None,
    user_id: int = None,
    limit: int = None,
    offset: int = None,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineのタイムエントリ一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await GetTimeEntriesTool.run(
        redmine_url,
        api_key,
        project_id,
        user_id,
        limit,
        offset,
    )


@mcp.tool()
async def create_user(
    login: str,
    firstname: str,
    lastname: str,
    mail: str,
    password: str = None,
    auth_source_id: int = None,
    mail_notification: str = None,
    must_change_passwd: bool = None,
    generate_password: bool = None,
    custom_fields: list = None,
    send_information: bool = None,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineユーザーを作成"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await CreateUserTool.run(
        redmine_url,
        api_key,
        login,
        firstname,
        lastname,
        mail,
        password,
        auth_source_id,
        mail_notification,
        must_change_passwd,
        generate_password,
        custom_fields,
        send_information,
    )


@mcp.tool()
async def delete_user(
    user_id: int,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineユーザーを削除"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await DeleteUserTool.run(
        redmine_url,
        api_key,
        user_id,
    )


@mcp.tool()
async def get_user(
    user_id: int,
    redmine_url: str = None,
    api_key: str = None,
) -> dict:
    """Redmineユーザー情報を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await GetUserTool.run(
        redmine_url,
        api_key,
        user_id,
    )


@mcp.tool()
async def get_users(
    redmine_url: str = None,
    api_key: str = None,
    name: str = None,
    group_id: int = None,
    status: int = None,
    limit: int = None,
    offset: int = None,
) -> dict:
    """Redmineユーザー一覧を取得"""
    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await GetUsersTool.run(
        redmine_url,
        api_key,
        name,
        group_id,
        status,
        limit,
        offset,
    )


@mcp.tool()
async def update_user(
    user_id: int,
    redmine_url: str = None,
    api_key: str = None,
    login: str = None,
    firstname: str = None,
    lastname: str = None,
    mail: str = None,
    password: str = None,
    auth_source_id: int = None,
    mail_notification: str = None,
    must_change_passwd: bool = None,
    generate_password: bool = None,
    custom_fields: list = None,
    status: int = None,
) -> dict:
    """Redmineユーザー情報を更新"""

    if redmine_url is None:
        redmine_url = os.environ.get("REDMINE_URL")
    if api_key is None:
        api_key = os.environ.get("REDMINE_ADMIN_API_KEY")
    return await UpdateUserTool.run(
        redmine_url,
        api_key,
        user_id,
        login,
        firstname,
        lastname,
        mail,
        password,
        auth_source_id,
        mail_notification,
        must_change_passwd,
        generate_password,
        custom_fields,
        status,
    )


if __name__ == "__main__":
    mcp.run()
