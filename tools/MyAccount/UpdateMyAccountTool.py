"""UpdateMyAccountTool

A Tool definition for updating the current user's account information in Redmine.
"""

from mcp import Tool

from tools.MyAccount.update_my_account import update_my_account

UpdateMyAccountTool = Tool.from_function(
    update_my_account,
    name="update_my_account",
    description="Update the current user's account information in Redmine.",
)
