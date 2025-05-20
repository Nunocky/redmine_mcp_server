from fastmcp.tools.tool import Tool

from tools.News.get_news_tool import get_news

GetNewsTool = Tool.from_function(
    get_news,
    name="get_news",
    description="Get a list of news from Redmine.",
)
