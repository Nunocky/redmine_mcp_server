from fastmcp.tools.tool import Tool

from tools.Trackers.get_trackers import get_trackers

GetTrackersTool = Tool.from_function(
    get_trackers,
    name="get_trackers",
    description="Get a list of trackers from Redmine.",
)
