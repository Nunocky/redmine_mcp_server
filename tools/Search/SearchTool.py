from fastmcp.tools.tool import Tool

from tools.Search.search import search

SearchTool = Tool.from_function(
    search,
    name="search",
    description="A tool for cross-resource search in Redmine. You can search for keywords across issues, projects, news, and wiki pages.",
)
