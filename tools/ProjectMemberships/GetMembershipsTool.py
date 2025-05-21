"""Redmineのプロジェクトメンバーシップ一覧取得ツールクラス"""

from mcp import Tool

from tools.ProjectMemberships.get_memberships_tool import get_memberships

GetMembershipsTool = Tool.from_function(
    get_memberships,
    name="get_memberships",
    description="Get memberships from Redmine",
)
