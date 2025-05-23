#!/usr/bin/env python3
"""MCP server entry point

Registers all API tools under tools as Redmine MCP server using @mcp.tool() and starts the server.
"""

from fastmcp.server import FastMCP

from tools.Attachments.DeleteAttachmentTool import DeleteAttachmentTool
from tools.Attachments.GetAttachmentTool import GetAttachmentTool
from tools.Attachments.UpdateAttachmentTool import UpdateAttachmentTool
from tools.Attachments.UploadAttachmentTool import UploadAttachmentTool
from tools.Enumerations.GetDocumentCategoriesTool import GetDocumentCategoriesTool
from tools.Enumerations.GetIssuePrioritiesTool import GetIssuePrioritiesTool
from tools.Enumerations.GetTimeEntryActivitiesTool import GetTimeEntryActivitiesTool
from tools.IssueRelations.GetIssueRelationsTool import GetIssueRelationsTool
from tools.Issues.AddWatcherTool import AddWatcherTool
from tools.Issues.CreateIssueTool import CreateIssueTool
from tools.Issues.DeleteIssueTool import DeleteIssueTool
from tools.Issues.GetIssuesTool import GetIssuesTool
from tools.Issues.GetIssueTool import GetIssueTool
from tools.Issues.RemoveWatcherTool import RemoveWatcherTool
from tools.Issues.UpdateIssueTool import UpdateIssueTool
from tools.IssueStatuses.GetIssueStatusesTool import GetIssueStatusesTool
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
from tools.Trackers.GetTrackersTool import GetTrackersTool
from tools.Users.CreateUserTool import CreateUserTool
from tools.Users.DeleteUserTool import DeleteUserTool
from tools.Users.get_users import GetUsersTool
from tools.Users.GetUserTool import GetUserTool
from tools.Users.UpdateUserTool import UpdateUserTool
from tools.Versions.GetVersionTool import GetVersionTool
from tools.WikiPages.GetWikiPagesTool import GetWikiPagesTool

from tools.Groups.GetGroupsTool import GetGroupsTool
from tools.Groups.CreateGroupTool import CreateGroupTool
from tools.Groups.GetGroupTool import GetGroupTool
from tools.Groups.UpdateGroupTool import UpdateGroupTool
from tools.Groups.DeleteGroupTool import DeleteGroupTool
from tools.Groups.AddUserToGroupTool import AddUserToGroupTool
from tools.Groups.RemoveUserFromGroupTool import RemoveUserFromGroupTool

mcp = FastMCP("Redmine MCP Server", "0.1.0")

# ProjectMemberships
mcp.add_tool(GetMembershipsTool.fn)
mcp.add_tool(CreateProjectMembershipTool.fn)

# News
mcp.add_tool(GetNewsTool.fn)

# IssueStatuses
mcp.add_tool(GetIssueStatusesTool.fn)

# Trackers
mcp.add_tool(GetTrackersTool.fn)

# Versions
mcp.add_tool(GetVersionTool.fn)

# WikiPages
mcp.add_tool(GetWikiPagesTool.fn)

# Issues
mcp.add_tool(GetIssueTool.fn)
mcp.add_tool(GetIssuesTool.fn)
mcp.add_tool(GetIssueRelationsTool.fn)
mcp.add_tool(CreateIssueTool.fn)
mcp.add_tool(UpdateIssueTool.fn)  # △
mcp.add_tool(DeleteIssueTool.fn)
mcp.add_tool(AddWatcherTool.fn)
mcp.add_tool(RemoveWatcherTool.fn)

# Queries (保存済み検索条件)
mcp.add_tool(GetQueriesTool.fn)

# Projects
mcp.add_tool(GetProjectsTool.fn)
mcp.add_tool(GetProjectTool.fn)
mcp.add_tool(CreateProjectTool.fn)
mcp.add_tool(UpdateProjectTool.fn)
mcp.add_tool(DeleteProjectTool.fn)
mcp.add_tool(ArchiveProjectTool.fn)
mcp.add_tool(UnarchiveProjectTool.fn)

# TimeEntries (作業時間記録)
mcp.add_tool(GetTimeEntriesTool.fn)
mcp.add_tool(CreateTimeEntryTool.fn)

# Attachments
mcp.add_tool(UploadAttachmentTool.fn)
mcp.add_tool(DeleteAttachmentTool.fn)
mcp.add_tool(GetAttachmentTool.fn)
mcp.add_tool(UpdateAttachmentTool.fn)  # skip

# Users
mcp.add_tool(GetUsersTool.fn)
mcp.add_tool(GetUserTool.fn)
mcp.add_tool(CreateUserTool.fn)
mcp.add_tool(UpdateUserTool.fn)
mcp.add_tool(DeleteUserTool.fn)

# Roles
mcp.add_tool(GetRolesTool.fn)
mcp.add_tool(GetRoleTool.fn)

# My Account
mcp.add_tool(GetMyAccountTool.fn)

# Enumerations
mcp.add_tool(GetIssuePrioritiesTool.fn)
mcp.add_tool(GetTimeEntryActivitiesTool.fn)
mcp.add_tool(GetDocumentCategoriesTool.fn)

# Groups
mcp.add_tool(GetGroupsTool.fn)
mcp.add_tool(CreateGroupTool.fn)
mcp.add_tool(GetGroupTool.fn)
mcp.add_tool(UpdateGroupTool.fn)
mcp.add_tool(DeleteGroupTool.fn)
mcp.add_tool(AddUserToGroupTool.fn)
mcp.add_tool(RemoveUserFromGroupTool.fn)

if __name__ == "__main__":
    mcp.run()
