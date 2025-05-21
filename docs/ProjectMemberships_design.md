# Project Memberships 機能 設計書

## 1. 要件定義

Redmineのプロジェクトメンバーシップ情報を操作するためのAPIクライアント機能を提供する。
具体的には、以下の操作を可能とする。

- [x] プロジェクトメンバーシップの一覧取得
- [x] プロジェクトメンバーシップの詳細取得
- [x] プロジェクトメンバーシップの更新
- [x] プロジェクトメンバーシップの作成
- [x] プロジェクトメンバーシップの削除

## 2. 設計書

### 2.1. 概略設計

Redmine APIの `/projects/:project_id/memberships` および `/memberships/:id` エンドポイントを利用して、プロジェクトメンバーシップのCRUD操作を行うためのツール群を開発する。
各ツールは、Redmine APIクライアントを通じてRedmineサーバーと通信する。

### 2.2. 機能設計

#### 2.2.1. プロジェクトメンバーシップ一覧取得 (get_project_memberships)

- **機能概要:** 指定されたプロジェクトのメンバーシップ一覧を取得する。
- **エンドポイント:** `GET /projects/:project_id/memberships.:format`
- **入力:**
    - `project_id` (必須): プロジェクトIDまたは識別子
    - `limit` (任意): 取得件数の上限
    - `offset` (任意): 取得開始位置
- **出力:** メンバーシップ情報のリスト
- **主要な処理:**
    1. Redmine APIクライアントを利用して、指定されたプロジェクトのメンバーシップ一覧を取得する。
    2. 取得結果を整形して返す。

#### 2.2.2. プロジェクトメンバーシップ作成 (create_project_membership)

- **機能概要:** 指定されたプロジェクトに新しいメンバーシップを作成する。
- **エンドポイント:** `POST /projects/:project_id/memberships.:format`
- **入力:**
    - `project_id` (必須): プロジェクトIDまたは識別子
    - `user_id` (必須): ユーザーIDまたはグループID
    - `role_ids` (必須): ロールIDの配列
- **出力:** 作成されたメンバーシップ情報、またはエラー情報（失敗時はエラー内容を含む dict を返す）
- **主要な処理:**
    1. Redmine APIクライアントを利用して、指定された情報で新しいメンバーシップを作成する。
    2. 作成結果（成功時はメンバーシップ情報、失敗時はエラー情報を含む dict）を返す。

#### 2.2.3. プロジェクトメンバーシップ詳細取得 (get_project_membership)

- **機能概要:** 指定されたIDのメンバーシップ詳細を取得する。
- **エンドポイント:** `GET /memberships/:id.:format`
- **入力:**
    - `membership_id` (必須): メンバーシップID
- **出力:** メンバーシップ詳細情報
- **主要な処理:**
    1. Redmine APIクライアントを利用して、指定されたIDのメンバーシップ詳細を取得する。
    2. 取得結果を整形して返す。

#### 2.2.4. プロジェクトメンバーシップ更新 (update_project_membership)

- **機能概要:** 指定されたIDのメンバーシップ情報を更新する。ロールのみ更新可能。
- **エンドポイント:** `PUT /memberships/:id.:format`
- **入力:**
    - `membership_id` (必須): メンバーシップID
    - `role_ids` (必須): 更新後のロールIDの配列
- **出力:** 更新成功時はステータスコード、失敗時はエラー情報
- **主要な処理:**
    1. Redmine APIクライアントを利用して、指定されたIDのメンバーシップ情報を更新する。
    2. 更新結果（成功時はステータスコード、失敗時はエラー情報）を返す。

#### 2.2.5. プロジェクトメンバーシップ削除 (delete_project_membership)

- **機能概要:** 指定されたIDのメンバーシップを削除する。
- **エンドポイント:** `DELETE /memberships/:id.:format`
- **入力:**
    - `membership_id` (必須): メンバーシップID
- **出力:** 削除成功時はステータスコード、失敗時はエラー情報
- **主要な処理:**
    1. Redmine APIクライアントを利用して、指定されたIDのメンバーシップを削除する。
    2. 削除結果（成功時はステータスコード、失敗時はエラー情報）を返す。

### 2.3. クラス構成（2025/05/21修正版）

- 各ツールはクラスベースから「関数＋Tool.from_function」パターンへ統一。
- 各API操作は `tools/ProjectMemberships/xxx.py` に関数として実装し、それを `Tool.from_function` でラップしたツール定義ファイル（`GetProjectMembershipTool.py` など）を用意。
- APIクライアント呼び出しは News系と同様、`redmine_url`・`api_key` を引数または環境変数から取得する関数型実装とする。

#### 実装例

```python
# tools/ProjectMemberships/get_project_membership.py
def get_project_membership(membership_id: int, redmine_url: Optional[str] = None, api_key: Optional[str] = None) -> dict:
    # ...（RedmineAPIClientでAPI呼び出し）
    return membership_info

# tools/ProjectMemberships/GetProjectMembershipTool.py
GetProjectMembershipTool = Tool.from_function(
    get_project_membership,
    name="get_project_membership",
    description="Get the details of a project membership from Redmine.",
)
```

#### 変更理由

- News系ツールと実装スタイルを統一し、保守性・テスト容易性を向上。
- クラスベースの execute() ではなく、関数型＋Tool.from_function でツール定義を一元化。


## 3. 注意事項

- グループから継承されたメンバーシップは、直接削除・更新できない場合がある。APIの仕様に従い、適切なエラーハンドリングを行う。
- APIキーとRedmine URLは、設定ファイルまたは環境変数から取得することを想定する。
