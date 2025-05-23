# Groups一覧取得・作成・詳細取得ツール設計書

## 要件定義

- Redmineのグループ一覧取得API（GET /groups.json）、グループ作成API（POST /groups.json）、グループ詳細取得API（GET /groups/{id}.json）をPythonツールとして実装する
- 認証情報（redmine_url, api_key）は必須
- レスポンスはJSON形式
- 例外処理、GoogleスタイルDocstring、PEP8、英語コメントを徹底
- 既存のtools/redmine_api_client.pyを利用

## 機能仕様

### グループ一覧取得
- APIエンドポイント: GET /groups.json
- 必須引数: redmine_url, api_key
- 任意引数: limit, offset, name
- レスポンス: Redmineのgroupsリスト（404時は空リスト）

### グループ作成
- APIエンドポイント: POST /groups.json
- 必須引数: redmine_url, api_key, name
- 任意引数: users（ユーザーIDリスト）, custom_fields（カスタムフィールド）
- レスポンス: 作成されたグループ情報（Redmine API仕様に準拠）

### グループ詳細取得
- APIエンドポイント: GET /groups/{id}.json
- 必須引数: redmine_url, api_key, group_id
- レスポンス: 指定グループの詳細情報（404時は group: None）

## クラス構成

- tools/Groups/get_groups.py: グループ一覧取得APIクライアント関数
- tools/Groups/GetGroupsTool.py: グループ一覧取得Toolクラス
- tools/Groups/create_group.py: グループ作成APIクライアント関数
- tools/Groups/CreateGroupTool.py: グループ作成Toolクラス
- tools/Groups/get_group.py: グループ詳細取得APIクライアント関数
- tools/Groups/GetGroupTool.py: グループ詳細取得Toolクラス
