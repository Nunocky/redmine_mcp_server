from fastmcp.tools.tool import Tool

from tools.Issues.remove_watcher_tool import remove_watcher

RemoveWatcherTool = Tool.from_function(
    remove_watcher,
    name="remove_watcher",
    description="Remove a watcher from a Redmine issue",
)
