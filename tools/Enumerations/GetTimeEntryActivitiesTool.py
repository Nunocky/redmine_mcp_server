from fastmcp.tools.tool import Tool

from .get_time_entry_activities import get_time_entry_activities

GetTimeEntryActivitiesTool = Tool.from_function(
    get_time_entry_activities,
    name="get_time_entry_activities",
    description="Get a list of time entry activities from Redmine.",
)
