from fastmcp.tools.tool import Tool

from tools.Queries.get_queries_tool import get_queries

GetQueriesTool = Tool.from_function(
    get_queries,
    name="get_queries",
    description="Get a list of queries from Redmine.",
)
