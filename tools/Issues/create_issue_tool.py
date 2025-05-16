"""Redmine課題作成ツール

Redmineの課題（Issue）を新規作成するツールです。
"""

from typing import Any, Dict, Optional
from tools.redmine_api_client import RedmineAPIClient

class CreateIssueTool:
    """Redmineの課題作成ツール

    Attributes:
        client (RedmineAPIClient): Redmine APIクライアント
    """

    def __init__(self, client: Optional[RedmineAPIClient] = None) -> None:
        """コンストラクタ

        Args:
            client (RedmineAPIClient, optional): APIクライアント。未指定時は新規生成。
        """
        self.client = client or RedmineAPIClient()

    def run(
        self,
        project_id: str,
        subject: str,
        description: Optional[str] = None,
        tracker_id: Optional[int] = None,
        status_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        category_id: Optional[int] = None,
        fixed_version_id: Optional[int] = None,
        assigned_to_id: Optional[int] = None,
        parent_issue_id: Optional[int] = None,
        custom_fields: Optional[Any] = None,
        watcher_user_ids: Optional[Any] = None,
        is_private: Optional[bool] = None,
        estimated_hours: Optional[float] = None,
        uploads: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """課題を新規作成する

        Args:
            project_id (str): プロジェクトID
            subject (str): 題名
            description (str, optional): 説明
            tracker_id (int, optional): トラッカーID
            status_id (int, optional): ステータスID
            priority_id (int, optional): 優先度ID
            category_id (int, optional): カテゴリID
            fixed_version_id (int, optional): バージョンID
            assigned_to_id (int, optional): 担当者ID
            parent_issue_id (int, optional): 親課題ID
            custom_fields (Any, optional): カスタムフィールド
            watcher_user_ids (Any, optional): ウォッチャーIDリスト
            is_private (bool, optional): プライベートフラグ
            estimated_hours (float, optional): 予定工数
            uploads (Any, optional): 添付ファイル

        Returns:
            dict: 作成された課題情報

        Raises:
            Exception: APIリクエスト失敗時
        """
        issue_data: Dict[str, Any] = {
            "project_id": project_id,
            "subject": subject,
        }
        if description:
            issue_data["description"] = description
        if tracker_id is not None:
            issue_data["tracker_id"] = tracker_id
        if status_id is not None:
            issue_data["status_id"] = status_id
        if priority_id is not None:
            issue_data["priority_id"] = priority_id
        if category_id is not None:
            issue_data["category_id"] = category_id
        if fixed_version_id is not None:
            issue_data["fixed_version_id"] = fixed_version_id
        if assigned_to_id is not None:
            issue_data["assigned_to_id"] = assigned_to_id
        if parent_issue_id is not None:
            issue_data["parent_issue_id"] = parent_issue_id
        if custom_fields:
            issue_data["custom_fields"] = custom_fields
        if watcher_user_ids:
            issue_data["watcher_user_ids"] = watcher_user_ids
        if is_private is not None:
            issue_data["is_private"] = is_private
        if estimated_hours is not None:
            issue_data["estimated_hours"] = estimated_hours
        if uploads:
            issue_data["uploads"] = uploads

        response = self.client.post(
            endpoint="/issues.json",
            json={"issue": issue_data},
        )
        return response.json()
