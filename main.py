"""MCP server entry point

Registers all API tools under tools as Redmine MCP server using @mcp.tool() and starts the server.
"""

from fastmcp.server import FastMCP

from tools.Attachments.delete_attachment_tool import DeleteAttachmentTool
from tools.Attachments.get_attachment_tool import GetAttachmentTool
from tools.Attachments.update_attachment_tool import UpdateAttachmentTool
from tools.Attachments.upload_attachment_tool import UploadAttachmentTool
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
from tools.News.get_news_tool import GetNewsTool
from tools.ProjectMemberships.create_membership_tool import CreateProjectMembershipTool
from tools.ProjectMemberships.get_memberships_tool import GetMembershipsTool
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

# こういう書き方のほうがいいかも
# tools = [
#     GetMembershipsTool,
#     CreateProjectMembershipTool,
#     GetNewsTool,
#     # ...他のTool...
# ]

# for tool in tools:
#     mcp.add_tool(tool.fn)

# ProjectMemberships
mcp.add_tool(GetMembershipsTool.fn)  # OK
mcp.add_tool(CreateProjectMembershipTool.fn)  # △ get_rolesが必要と言われる

# News
mcp.add_tool(GetNewsTool.fn)  # OK

# Versions
mcp.add_tool(GetVersionTool.fn)  # 多分OK

# WikiPages
mcp.add_tool(GetWikiPagesTool.fn)  # OK

# Issues
mcp.add_tool(GetIssueTool.fn)  # OK
mcp.add_tool(GetIssuesTool.fn)  # OK
mcp.add_tool(GetIssueRelationsTool.fn)  # OK
mcp.add_tool(CreateIssueTool.fn)  # OK
mcp.add_tool(UpdateIssueTool.fn)  # △
mcp.add_tool(DeleteIssueTool.fn)  # OK
mcp.add_tool(AddWatcherTool.fn)  # OK
mcp.add_tool(RemoveWatcherTool.fn)

# Queries
mcp.add_tool(GetQueriesTool.fn)

# Projects
mcp.add_tool(GetProjectsTool.fn)  # OK
mcp.add_tool(GetProjectTool.fn)  # OK
mcp.add_tool(CreateProjectTool.fn)  # OK
mcp.add_tool(UpdateProjectTool.fn)  # OK
mcp.add_tool(DeleteProjectTool.fn)  # OK
mcp.add_tool(ArchiveProjectTool.fn)  # OK
mcp.add_tool(UnarchiveProjectTool.fn)  # OK

# TimeEntries
mcp.add_tool(GetTimeEntriesTool.fn)
mcp.add_tool(CreateTimeEntryTool.fn)

# Attachments
mcp.add_tool(DeleteAttachmentTool.fn)
mcp.add_tool(GetAttachmentTool.fn)
mcp.add_tool(UpdateAttachmentTool.fn)
mcp.add_tool(UploadAttachmentTool.fn)

# Users
mcp.add_tool(GetUsersTool.fn)
mcp.add_tool(GetUserTool.fn)
mcp.add_tool(CreateUserTool.fn)
mcp.add_tool(UpdateUserTool.fn)
mcp.add_tool(DeleteUserTool.fn)


if __name__ == "__main__":
    mcp.run()
