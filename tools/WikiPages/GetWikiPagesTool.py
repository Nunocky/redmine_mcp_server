from fastmcp.tools.tool import Tool

from tools.WikiPages.get_wiki_pages import get_wiki_pages

GetWikiPagesTool = Tool.from_function(
    get_wiki_pages,
    name="get_wiki_pages",
    description="Get wiki pages from Redmine",
)
