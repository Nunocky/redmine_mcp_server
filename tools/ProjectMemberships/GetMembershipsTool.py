"""Redmineのプロジェクトメンバーシップ一覧取得ツールクラス"""

from fastmcp.tools.tool import Tool

from tools.ProjectMemberships.get_memberships import get_memberships

GetMembershipsTool = Tool.from_function(
    get_memberships,
    name="get_memberships",
    description="Get memberships from Redmine",
)
