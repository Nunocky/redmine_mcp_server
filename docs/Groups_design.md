# Groups一覧取得ツール設計書

## 要件定義

- Redmineのグループ一覧取得API（GET /groups.json）をPythonツールとして実装する
- 認証情報（redmine_url, api_key）は必須
- レスポンスはJSON形式
- 例外処理、GoogleスタイルDocstring、PEP8、英語コメントを徹底
- 既存のtools/redmine_api_client.pyを利用

## 機能仕様

- APIエンドポイント: GET /groups.json
- 必須引数: redmine_url, api_key
- 任意引数: limit, offset, name
- レスポンス: Redmineのgroupsリスト（404時は空リスト）

## クラス構成

- tools/Groups/get_groups.py: APIクライアント関数
- tools/Groups/GetGroupsTool.py: Toolクラス
