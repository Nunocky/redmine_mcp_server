from fastmcp.tools.tool import Tool

from tools.TimeEntries.create_time_entry import create_time_entry

CreateTimeEntryTool = Tool.from_function(
    create_time_entry,
    name="create_time_entry",
    description="Create a new time entry in Redmine.",
)
