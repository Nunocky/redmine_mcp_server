from fastmcp.tools.tool import Tool

from tools.TimeEntries.get_time_entries import get_time_entries

GetTimeEntriesTool = Tool.from_function(
    get_time_entries,
    name="get_time_entries",
    description="Retrieve a list of time entries from Redmine.",
)
