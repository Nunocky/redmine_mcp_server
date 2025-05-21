#!/usr/bin/env python3
"""MCP server entry point

Registers all API tools under tools as Redmine MCP server using @mcp.tool() and starts the server.
"""

from fastmcp.server import FastMCP

from tools.Attachments.DeleteAttachmentTool import DeleteAttachmentTool
from tools.Attachments.GetAttachmentTool import GetAttachmentTool
from tools.Attachments.UpdateAttachmentTool import UpdateAttachmentTool
from tools.Attachments.UploadAttachmentTool import UploadAttachmentTool
from tools.Issues.AddWatcherTool import AddWatcherTool
from tools.Issues.CreateIssueTool import CreateIssueTool
from tools.Issues.DeleteIssueTool import DeleteIssueTool
from tools.Issues.GetIssueRelationsTool import GetIssueRelationsTool
from tools.Issues.GetIssuesTool import GetIssuesTool
from tools.Issues.GetIssueTool import GetIssueTool
from tools.Issues.RemoveWatcherTool import RemoveWatcherTool
from tools.Issues.UpdateIssueTool import UpdateIssueTool
from tools.MyAccount.GetMyAccountTool import GetMyAccountTool
from tools.News.GetNewsTool import GetNewsTool
from tools.ProjectMemberships.CreateProjectMembershipTool import CreateProjectMembershipTool
from tools.ProjectMemberships.GetMembershipsTool import GetMembershipsTool
from tools.Projects.ArchiveProjectTool import ArchiveProjectTool
from tools.Projects.CreateProjectTool import CreateProjectTool
from tools.Projects.DeleteProjectTool import DeleteProjectTool
from tools.Projects.get_projects import GetProjectsTool
from tools.Projects.GetProjectTool import GetProjectTool
from tools.Projects.UnarchiveProjectTool import UnarchiveProjectTool
from tools.Projects.UpdateProjectTool import UpdateProjectTool
from tools.Queries.GetQueriesTool import GetQueriesTool
from tools.Roles.GetRolesTool import GetRolesTool
from tools.Roles.GetRoleTool import GetRoleTool
from tools.TimeEntries.CreateTimeEntryTool import CreateTimeEntryTool
from tools.TimeEntries.GetTimeEntriesTool import GetTimeEntriesTool
from tools.Users.CreateUserTool import CreateUserTool
from tools.Users.DeleteUserTool import DeleteUserTool
from tools.Users.get_users import GetUsersTool
from tools.Users.GetUserTool import GetUserTool
from tools.Users.UpdateUserTool import UpdateUserTool
from tools.Versions.GetVersionTool import GetVersionTool
from tools.WikiPages.GetWikiPagesTool import GetWikiPagesTool

mcp = FastMCP("Redmine MCP Server", "0.1.0")

# こういう書き方のほうがいいかも
# tools = [
#     # ProjectMemberships
#     GetMembershipsTool,
#     CreateProjectMembershipTool,
#     # News
#     GetNewsTool,
#     # Versions
#     GetVersionTool,
#     # WikiPages
#     GetWikiPagesTool,
#     # Issues
#     GetIssueTool,
#     GetIssuesTool,
#     GetIssueRelationsTool,
#     CreateIssueTool,
#     UpdateIssueTool,  # △
#     DeleteIssueTool,
#     AddWatcherTool,
#     RemoveWatcherTool,
#     # Queries
#     GetQueriesTool,
#     # Projects
#     GetProjectsTool,
#     GetProjectTool,
#     CreateProjectTool,
#     UpdateProjectTool,
#     DeleteProjectTool,
#     ArchiveProjectTool,
#     UnarchiveProjectTool,
#     # TimeEntries
#     GetTimeEntriesTool,
#     CreateTimeEntryTool,
#     # Attachments
#     DeleteAttachmentTool,
#     GetAttachmentTool,
#     UpdateAttachmentTool,
#     UploadAttachmentTool,
#     # Users
#     GetUsersTool,
#     GetUserTool,
#     CreateUserTool,
#     UpdateUserTool,
#     DeleteUserTool,
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
mcp.add_tool(RemoveWatcherTool.fn)  # OK

# Queries (保存済み検索条件)
mcp.add_tool(GetQueriesTool.fn)  # OK

# Projects
mcp.add_tool(GetProjectsTool.fn)  # OK
mcp.add_tool(GetProjectTool.fn)  # OK
mcp.add_tool(CreateProjectTool.fn)  # OK
mcp.add_tool(UpdateProjectTool.fn)  # OK
mcp.add_tool(DeleteProjectTool.fn)  # OK
mcp.add_tool(ArchiveProjectTool.fn)  # OK
mcp.add_tool(UnarchiveProjectTool.fn)  # OK

# TimeEntries (作業時間記録)
mcp.add_tool(GetTimeEntriesTool.fn)  # OK
mcp.add_tool(CreateTimeEntryTool.fn)  # OK

# Attachments
mcp.add_tool(UploadAttachmentTool.fn)  # OK
mcp.add_tool(DeleteAttachmentTool.fn)  # OK
mcp.add_tool(GetAttachmentTool.fn)  # OK
mcp.add_tool(UpdateAttachmentTool.fn)  # skip

# Users
mcp.add_tool(GetUsersTool.fn)  # OK
mcp.add_tool(GetUserTool.fn)  # OK
mcp.add_tool(CreateUserTool.fn)  # OK
mcp.add_tool(UpdateUserTool.fn)  # OK
mcp.add_tool(DeleteUserTool.fn)  # OK

# Roles
mcp.add_tool(GetRolesTool.fn)  # OK
mcp.add_tool(GetRoleTool.fn)  # OK

# My Account
mcp.add_tool(GetMyAccountTool.fn)  # OK

if __name__ == "__main__":
    mcp.run()
