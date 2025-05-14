"""MCPサーバエントリポイント

Redmine MCPサーバとしてtools配下の全APIツールを登録し、サーバを起動する。
"""

from mcp import serve, Tool
from tools.get_issues_tool import GetIssuesTool
from tools.create_issue_tool import create_issue
from tools.update_issue_tool import update_issue
from tools.delete_issue_tool import delete_issue
from tools.get_issue_relations_tool import GetIssueRelationsTool
from tools.get_projects_tool import get_projects
from tools.get_project_tool import get_project
from tools.create_project_tool import create_project
from tools.update_project_tool import update_project
from tools.delete_project_tool import delete_project
from tools.archive_project_tool import archive_project
from tools.unarchive_project_tool import unarchive_project
from tools.get_users_tool import get_users
from tools.get_memberships_tool import get_memberships
from tools.get_news_tool import GetNewsTool
from tools.get_queries_tool import GetQueriesTool
from tools.get_time_entries_tool import get_time_entries
from tools.get_versions_tool import GetVersionsTool
from tools.get_wiki_pages_tool import GetWikiPagesTool
from tools.add_watcher_tool import add_watcher
from tools.remove_watcher_tool import remove_watcher

TOOLS = [
    Tool(
        name="get_issues",
        description="Get a list of Redmine issues.",
        entrypoint=GetIssuesTool().run,
        parameters={},
        returns={"type": "object", "description": "課題一覧とページ情報"},
    ),
    Tool(
        name="create_issue",
        description="Create a new Redmine issue.",
        entrypoint=create_issue,
        parameters={},
        returns={"type": "object", "description": "作成された課題情報"},
    ),
    Tool(
        name="update_issue",
        description="Update an existing Redmine issue.",
        entrypoint=update_issue,
        parameters={},
        returns={"type": "object", "description": "更新後の課題情報"},
    ),
    Tool(
        name="delete_issue",
        description="Delete a Redmine issue.",
        entrypoint=delete_issue,
        parameters={},
        returns={"type": "object", "description": "削除結果"},
    ),
    Tool(
        name="get_issue_relations",
        description="Get relations of a Redmine issue.",
        entrypoint=GetIssueRelationsTool().run,
        parameters={},
        returns={"type": "object", "description": "課題関連情報"},
    ),
    Tool(
        name="get_projects",
        description="Get a list of Redmine projects.",
        entrypoint=get_projects,
        parameters={},
        returns={"type": "object", "description": "プロジェクト一覧"},
    ),
    Tool(
        name="get_project",
        description="Get details of a Redmine project.",
        entrypoint=get_project,
        parameters={},
        returns={"type": "object", "description": "プロジェクト詳細"},
    ),
    Tool(
        name="create_project",
        description="Create a new Redmine project.",
        entrypoint=create_project,
        parameters={},
        returns={"type": "object", "description": "作成されたプロジェクト情報"},
    ),
    Tool(
        name="update_project",
        description="Update an existing Redmine project.",
        entrypoint=update_project,
        parameters={},
        returns={"type": "object", "description": "更新後のプロジェクト情報"},
    ),
    Tool(
        name="delete_project",
        description="Delete a Redmine project.",
        entrypoint=delete_project,
        parameters={},
        returns={"type": "object", "description": "削除結果"},
    ),
    Tool(
        name="archive_project",
        description="Archive a Redmine project.",
        entrypoint=archive_project,
        parameters={},
        returns={"type": "object", "description": "アーカイブ結果"},
    ),
    Tool(
        name="unarchive_project",
        description="Unarchive a Redmine project.",
        entrypoint=unarchive_project,
        parameters={},
        returns={"type": "object", "description": "アンアーカイブ結果"},
    ),
    Tool(
        name="get_users",
        description="Get a list of Redmine users.",
        entrypoint=get_users,
        parameters={},
        returns={"type": "object", "description": "ユーザー一覧"},
    ),
    Tool(
        name="get_memberships",
        description="Get memberships of a Redmine project.",
        entrypoint=get_memberships,
        parameters={},
        returns={"type": "object", "description": "メンバーシップ一覧"},
    ),
    Tool(
        name="get_news",
        description="Get a list of Redmine news.",
        entrypoint=GetNewsTool().run,
        parameters={},
        returns={"type": "object", "description": "ニュース一覧"},
    ),
    Tool(
        name="get_queries",
        description="Get a list of Redmine queries.",
        entrypoint=GetQueriesTool().run,
        parameters={},
        returns={"type": "object", "description": "クエリ一覧"},
    ),
    Tool(
        name="get_time_entries",
        description="Get a list of Redmine time entries.",
        entrypoint=get_time_entries,
        parameters={},
        returns={"type": "object", "description": "工数一覧"},
    ),
    Tool(
        name="get_versions",
        description="Get a list of Redmine versions.",
        entrypoint=GetVersionsTool().run,
        parameters={},
        returns={"type": "object", "description": "バージョン一覧"},
    ),
    Tool(
        name="get_wiki_pages",
        description="Get a list of Redmine wiki pages.",
        entrypoint=GetWikiPagesTool().run,
        parameters={},
        returns={"type": "object", "description": "Wikiページ一覧"},
    ),
    Tool(
        name="add_watcher",
        description="Redmine課題にウォッチャーを追加する",
        entrypoint=add_watcher,
        parameters={},
        returns={"type": "object", "description": "ウォッチャー追加結果"},
    ),
    Tool(
        name="remove_watcher",
        description="Redmine課題からウォッチャーを削除する",
        entrypoint=remove_watcher,
        parameters={},
        returns={"type": "object", "description": "ウォッチャー削除結果"},
    ),
]

if __name__ == "__main__":
    serve(tools=TOOLS)
