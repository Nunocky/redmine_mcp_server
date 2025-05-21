from fastmcp.tools.tool import Tool

from tools.Issues.add_watcher import add_watcher

AddWatcherTool = Tool.from_function(
    add_watcher,
    name="add_watcher",
    description="Add a watcher to a Redmine issue",
)
