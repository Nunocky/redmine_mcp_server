#!/usr/bin/env python3
from fastmcp.server import FastMCP

from tools.create_issue_tool import CreateIssueTool
from tools.delete_issue_tool import DeleteIssueTool
from tools.get_issues_tool import GetIssuesTool
from tools.get_memberships_tool import GetMembershipsTool
from tools.get_projects_tool import GetProjectsTool
from tools.get_time_entries_tool import GetTimeEntriesTool
from tools.get_users_tool import GetUsersTool
from tools.update_issue_tool import UpdateIssueTool

server = FastMCP(
    name="redmine-mcp-server",
    instructions="An MCP server for accessing the Redmine API.",
    tools=[
        GetIssuesTool,
        CreateIssueTool,
        UpdateIssueTool,
        DeleteIssueTool,
        GetProjectsTool,
        GetUsersTool,
        GetTimeEntriesTool,
        GetMembershipsTool,
    ],
)

if __name__ == "__main__":
    server.run()
