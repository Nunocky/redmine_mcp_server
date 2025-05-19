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

# ProjectMemberships
mcp.add_tool(GetMembershipsTool)
mcp.add_tool(CreateProjectMembershipTool)

# News
mcp.add_tool(GetNewsTool)

# Versions
mcp.add_tool(GetVersionTool)

# WikiPages
mcp.add_tool(GetWikiPagesTool)

# Issues
mcp.add_tool(GetIssueTool)
mcp.add_tool(GetIssuesTool)
mcp.add_tool(GetIssueRelationsTool)
mcp.add_tool(CreateIssueTool)
mcp.add_tool(UpdateIssueTool)
mcp.add_tool(DeleteIssueTool)
mcp.add_tool(AddWatcherTool)
mcp.add_tool(RemoveWatcherTool)

# Queries
mcp.add_tool(GetQueriesTool)

# Projects
mcp.add_tool(GetProjectsTool)
mcp.add_tool(GetProjectTool)
mcp.add_tool(CreateProjectTool)
mcp.add_tool(UpdateProjectTool)
mcp.add_tool(DeleteProjectTool)
mcp.add_tool(ArchiveProjectTool)
mcp.add_tool(UnarchiveProjectTool)

# TimeEntries
mcp.add_tool(GetTimeEntriesTool)
mcp.add_tool(CreateTimeEntryTool)

# Attachments
mcp.add_tool(DeleteAttachmentTool)
mcp.add_tool(GetAttachmentTool)
mcp.add_tool(UpdateAttachmentTool)
mcp.add_tool(UploadAttachmentTool)

# Users
mcp.add_tool(GetUsersTool)
mcp.add_tool(GetUserTool)
mcp.add_tool(CreateUserTool)
mcp.add_tool(UpdateUserTool)
mcp.add_tool(DeleteUserTool)


if __name__ == "__main__":
    mcp.run()
