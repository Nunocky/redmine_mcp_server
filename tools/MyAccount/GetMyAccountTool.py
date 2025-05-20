"""GetMyAccountTool

A Tool definition for getting the current user's account information from Redmine.
"""

from fastmcp.tools.tool import Tool

from tools.MyAccount.get_my_account_tool import get_my_account

GetMyAccountTool = Tool.from_function(
    get_my_account,
    name="get_my_account",
    description="Get the current user's account information from Redmine.",
)
